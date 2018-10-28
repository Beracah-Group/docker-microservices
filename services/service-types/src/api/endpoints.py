# add servicing mode
@app.route('/servicetypes/api/mode', methods=['POST'])
def add_mode():
    request.get_json(force=True)
        s_mode = request.json['mode']
        if not s_mode:
            response = jsonify({'Error': 'Servicing mode has no name'})
            response.status_code = 400
            return response

        res = Servicetypes.query.all()
        data_check = [data for data in res if data.mode == s_mode]
        if data_check:
            response = jsonify({'Warning': 'this service mode already exists.'})
            response.status_code = 409
            return response
        else:
            s = Servicetypes(mode=s_mode)
            s.save()
            response = jsonify({'status': 'Service mode added successfully'})
            response.status_code = 201
            return response
    except KeyError:
        response = jsonify({'Error': 'Use the name for dict key.'})
        response.status_code = 500
        return response

# get servicing mode
@app.route('/servicetypes/api/mode', methods=['GET'])
def retrieve_mode():
    message = 'No serviving modes have been created'

    limit = int(request.args.get("limit", 20))
    if limit > 100:
        limit = 100
    respons = Servicetypes.query.all()
    if not respons:
        response = jsonify({'error': 'No mode has been created yet'})
        response.status_code = 200
        return response
    else:
        search = request.args.get("q", "")
        if search:
            res = [mode for mode in respons if mode.mode in search]
            if not res:
                response = jsonify({'error': 'The service type you searched does not exist'})
                return response
            else:
                mode_data = []
                for data in res:
                    final = {
                        'id': data.id,
                        'mode': data.mode,
                        'description': data.description
                    }
                    mode_data.clear()
                    mode_data.append(final)
                response = jsonify(mode_data)
                response.status_code = 200
                return response
        else:
            res = [mode for mode in respons]
            mode_data = []
            if not res:
                response = jsonify({'error': message})
                response.status_code = 200
                return response
            else:
                for data in res:
                    final = {
                        'id': data.id,
                        'mode': data.mode,
                        'description': data.description
                    }
                    mode_data.append(final)
                response = jsonify(mode_data)
                response.status_code = 200
                return response


# get update delete servicing mode
@app.route('/servicetypes/api/mode/<int:mode_id>', methods=['GET', 'PUT', 'DELETE'])
def mode_by_id(mode_id):
    res = Servicetypes.query.all()
    mode_data = [mode for mode in res if mode.id == mode_id]
    if request.method == 'GET':
        data = {}
        for data in mode_data:
            data = {
                'id': data.id,
                'mode': data.mode,
                'description': data.description
            }
        if mode_id not in data.values():
            response = jsonify({'warning': 'the service mode does not exist.'})
            response.status_code = 404
            return response
        else:
            response = jsonify(data)
            response.status_code = 200
            return response
    elif request.method == 'DELETE':
        data = {}
        for data in mode_data:
            data = {
                'id': data.id,
                'mode': data.mode,
                'description': data.description
            }
        if mode_id not in data.values():
            response = jsonify({'warning': 'the mode does not exist.'})
            response.status_code = 404
            return response
        else:
            delete = Servicetypes.query.filter_by(id=mode_id).first()
            db.session.delete(delete)
            db.session.commit()
            response = jsonify({'Status': 'Servicing mode deleted successfully.'})
            response.status_code = 200
            return response
    elif request.method == 'PUT':
        request.get_json(force=True)
        data = Servicetypes.query.filter_by(id=mode_id).first()
        if not data:
            response = jsonify({'warning': 'the servicing mode does not exist.'})
            response.status_code = 404
            return response
        else:
            try:
                name = request.json['mode']
                data.name = name
                db.session.commit()
                data = {}
                for data in mode_data:
                    data = {
                        'id': data.id,
                        'mode': data.mode,
                        'description': data.description
                    }
                response = jsonify(data)
                response.status_code = 201
                return response
            except KeyError: 
                response = jsonify({'error': 'Please use name for dict keys.'})
                response.status_code = 500
                return response
