from flask import Blueprint, render_template, request
from .auth import isValidateRequest
from .models import Recipe, RecipeSchema
from datetime import datetime
from . import db

main = Blueprint('main', __name__)
recipe_schema = RecipeSchema(many=True)


@main.route('/')
def index():
    return "Welcome to your Recipe Book", 200


@main.route('/profile', methods=['GET'])
def get_profile():
    if isValidateRequest(request.authorization.username, request.authorization.password):
        recipes = Recipe.query.filter_by(username=request.authorization.username).all()
        return recipe_schema.dump(recipes), 200
    else:
        return 'Unauthorized', 401


@main.route('/search/recipe', methods=['GET'])
def get_search_recipe():
    query = getSearchQuery(request)
    if query['result']:
        recipes = query['message'].all()
        return recipe_schema.dump(recipes), 200
    else:
        return query['message'], 400


@main.route('/recipe', methods=['POST'])
def post_recipe():
    if isValidateRequest(request.authorization.username, request.authorization.password):
        isValidRecipe = validateRecipe(request)
        if isValidRecipe['result']:
            json = request.json
            recipename = json['recipename']
            ingredients = json['ingredients']
            instructions = json['instructions']
            servingsize = json['servingsize']
            category = json['category']
            notes = json['notes']

            recipe = Recipe.query.filter_by(username=request.authorization.username, recipename=recipename).first()
            if recipe:
                return 'Recipe exists. Id : ' + str(recipe.id) + ' :: Recipe Name : ' + recipe.recipename, 409
            else:
                newRecipe = Recipe(username=request.authorization.username, recipename=recipename,
                                   ingredients=str(ingredients), instructions=instructions, servingsize=servingsize,
                                   category=category, notes=notes)
                db.session.add(newRecipe)
                db.session.commit()
            return 'Recipe added : ' + recipename, 201
        else:
            return isValidRecipe['message'], 400
    else:
        return 'Unauthorized', 401


@main.route('/update/<id>', methods=['PUT'])
def put_update_recipe(id):
    if isValidateRequest(request.authorization.username, request.authorization.password) and isValidateUpdateId(id):
        recipe = Recipe.query.filter_by(id=id, username=request.authorization.username).first()
        if recipe:
            isValidUpdateReq = validateRecipe(request)
            if isValidUpdateReq['result']:
                req_json = request.json
                for arg in req_json:
                    if arg == 'ingredients':
                        recp_ing = eval(recipe.ingredients)
                        req_ing = req_json[arg]
                        result = updateIngredients(recp_ing, req_ing)
                        if result['result']:
                            recipe.ingredients = result['message']
                        else:
                            return result['message'], 404
                    elif arg == 'category':
                        recipe.category = req_json[arg]

                    elif arg == 'notes':
                        recipe.notes = req_json[arg]

                    elif arg == 'recipename':
                        recipe.recipename = req_json[arg]

                    elif arg == 'servingsize':
                        recipe.servingsize = req_json[arg]
            else:
                return isValidUpdateReq['message'], 400

            recipe.datemodified = datetime.utcnow()
            db.session.commit()
            return 'Recipe updated successfully : ' + recipe.recipename, 200
        else:
            return 'Recipe not found. Id : ' + id, 404
    else:
        return 'Invalid update id : ' + id, 400


@main.route('/delete/<id>', methods=['DELETE'])
def delete_delete_recipe(id):
    if (isValidateRequest(request.authorization.username, request.authorization.password) and isValidateUpdateId(id)):
        recipe = Recipe.query.filter_by(id=id, username=request.authorization.username).first()
        if recipe:
            db.session.delete(recipe)
            db.session.commit();
            return 'Recipe Deleted Successfully'
        else:
            return 'Recipe not found. Id : ' + id, 404
    else:
        return 'Invalid id : ' + id, 400

def updateIngredients(recp_ing, req_ing):
    for ing in req_ing:
        if ing == 'remove':
            for item in req_ing['remove']:
                if item in recp_ing:
                    recp_ing.pop(item)
                else:
                    return {'result': False, 'message': 'Item not found to remove : ' + item}
        else:
            recp_ing[ing] = req_ing[ing]
    return {'result': True, 'message': str(recp_ing)}

def validateRecipe(request):
    method = request.method
    recipe = request.json
    if method == 'POST':
        mandatory_fields = ['category', 'ingredients', 'instructions', 'recipename', 'servingsize']
        for field in mandatory_fields:
            if field not in recipe:
                return {'result': False, 'message': field+' is a mandatory field'}

    return validateRecipeBody(recipe)


def validateRecipeBody(recipe):
    units = ['count', 'gm', 'ml', 'l', 'inch', 'tsp', 'tbsp']
    recipe_category = ['breakfast', 'lunch', 'dinner']

    for entry in recipe:
        if entry == 'category':
            if recipe['category'] not in recipe_category:
                return {'result': False, 'message': 'Invalid recipe category : ' + recipe['category']}
        if entry == 'ingredients':
            for ing in recipe['ingredients']:
                if ing != 'remove':
                    if not isinstance(recipe['ingredients'][ing]['quantity'], (int, float)):
                        return {'result': False, 'message': 'Quantity for ingredient ' + ing + ' should be numeric'}
                    if recipe['ingredients'][ing]['unit'] not in units:
                        return {'result': False,
                            'message': 'Invalid unit ' + recipe['ingredients'][ing]['unit'] + ' for ingredient ' + ing+'. Please use any of these units : '+str(units)}
        if entry == 'instructions':
            if recipe['instructions'] == '':
                return {'result': False, 'message': 'Instructions can not be empty'}
        if entry == 'notes':
            if len(recipe['notes']) > 100:
                return {'result': False, 'message': 'Notes can not be longer than 100 characters'}
        if entry == 'recipename':
            if recipe['recipename'] == '':
                return {'result': False, 'message': 'Recipe name can not be empty'}
        if entry == 'servingsize':
            if recipe['servingsize'] == '':
                return {'result': False, 'message': 'Servingsize can not be empty'}

    return {'result': True}


def isValidateUpdateId(id):
    if id and id.isnumeric():
        return True
    else:
        return False


def getSearchQuery(request):
    args = request.args
    query = db.session.query(Recipe).filter(Recipe.username == request.authorization.username)
    for arg in args.to_dict():
        if arg == 'recipename':
            query = query.filter(Recipe.recipename.like('%' + args['recipename'] + '%'))
        elif arg == 'id':
            query = query.filter(Recipe.id == args['id'])
        elif arg == 'category':
            query = query.filter(Recipe.category == args['category'])
        elif arg == 'servingsize':
            query = query.filter(Recipe.servingsize == args['servingsize'])
        elif arg == 'before':
            search_date = datetime.strptime(args['before'], "%Y-%m-%d")
            query = query.filter(Recipe.dateposted < search_date)
        elif arg == 'after':
            search_date = datetime.strptime(args['after'], "%Y-%m-%d")
            query = query.filter(Recipe.dateposted > search_date)
        elif arg == 'between':
            search_dates = args['between']
            from_date = datetime.strptime(search_dates.split(',')[0], "%Y-%m-%d")
            to_date = datetime.strptime(search_dates.split(',')[1], "%Y-%m-%d")
            query = query.filter(Recipe.dateposted.between(from_date, to_date))
        else:
            return {'result': False, 'message': 'Invalid search parameter: ' + arg+'. Please use any of these params : category, recipename, servingsize or id.'}

    return {'result': True, 'message': query}
