from flask import jsonify, request, Response, abort
from app import app
from flask_login import login_required, current_user
from app.mongoDB import Device, User, ValidationError
from app.API.utils import doesnt_exist

""" These API are meant to be accessed from the web client 'Dashboard' """
# : These API are authenticated with a session, Should authenticate with key


@app.route("/api/v1/devices", methods=["GET", "POST"])
@login_required
def devices():

    if request.method == "GET":
        devices = Device.by_owner(current_user)
        return jsonify(devices)

    if request.method == "POST":
        """Create new device. Example:
            POST the JSON "{'port': 14, 'name': 'TV', 'place': 'room2', 'type': 1}"
            return device object if data is valid
            if the port already has a device update to the new parameters
        """
        args = request.get_json()
        port = args.get('port')
        name = args.get('name')
        place = args.get('place')
        d_type = args.get('type')

        # TODO: check if data is valid

        new_device = Device(name=name, port=port, place=place, d_type=d_type)
        try:
            new_device.save()
        except ValidationError as e:
            return jsonify(), 403
        return jsonify(), 201


@app.route("/api/v1/device", methods=["GET", "PUT", "DELETE"])
@login_required
def device():
    """ Access specific device by its key"""

    args = request.get_json()
    key = args["key"]
    port = args["port"]
    target_device = Device.by_key(key)

    if target_device is None:
        return jsonify(), 404

    if request.method == "GET":
        return jsonify(target_device)

    if request.method == "PUT":
        target_device.name = args['name']
        target_device.port = args['port']
        target_device.d_type = args['type']
        target_device.place = args['place']
        target_device.save()
        return jsonify(target_device)
    
    if request.method == "DELETE":
        target_device.delete()
        return jsonify("deleted"), 204
        

@app.route("/api/v1/device/action", methods=["PUT"])
@login_required
def deviceaction():
    """ Turn on / Turn off device from the Dashboard
    Example : PUT -d '{hub_id: 123abc, port: 10, is_on: True}'
    :return 200
    TODO return updated code with no body
    """

    args = request.get_json()
    hub_id = args["hub_id"]
    port = args['port']
    is_on = args['is_on']
    hub = {} # Hub.by_id(hub_id)
    target_device = {} # hub.get_device(port)

    if target_device is None:
        return doesnt_exist(port=port)
    target_device.is_on = is_on
    hub.save()
    # convert object id to string
    # target_device.id = str(target_device.id)
    return target_device.to_json()
