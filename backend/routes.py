from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return array of picture URLs"""
    if data:
        return (data,200)

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """return a picture as json"""
    if data:
        for pic in data:
            if pic["id"] == id:
                return (pic,200)
        return ({"message": f"Picture {id} not found."}, 404)

    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """create a picture resource as json"""
    input_pic = request.json
    print (input_pic)
    if data:
        for pic in data:
            if pic["id"] == input_pic["id"]:
                return ({"Message": f"picture with id {pic['id']} already present"},302)
        data.append(input_pic)
        return (input_pic, 201)
    
    return {"message": "Internal server error"}, 500
    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """update a picture resource as json"""
    input_pic = request.json
    if data:
        for i, pic in enumerate(data):
            if pic["id"] == id and input_pic["id"] == id:
                data[i] = input_pic
                return ({"Message": f"OK. Picture updated."},200)
        return ({"message": "picture not found"}, 404)

    return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """delete a picture as json"""
    if data:
        for i, pic in enumerate(data):
            if pic["id"] == id:
                data.pop(i)
                return ("",204)
        return ({"message": "picture not found"}, 404)

    return {"message": "Internal server error"}, 500
