from flask import Flask, request
from flask_restful import Resource, Api, marshal_with
from flask_cors import CORS
from interface import RunContainer
import requests

app = Flask(__name__)
CORS(app)
api = Api(app)



class CreateRandomContainer(Resource):
    def get(self):
        ret = RunContainer.SpinContainer(RunContainer.findRandomAvailablePort())
        print(ret)
        owner_id = "root"
        retu = requests.post("http://localhost:3000/docker", json={"port":ret[0],"name":ret[1],"owner_id":owner_id})
        ret.append(owner_id)
        return ret

class StopContainer(Resource):
    def get(self, id):
        ret = RunContainer.SpinDownContainer(id)
        print(ret)
        return ret

class PruneContainer(Resource):
    def get(self,id):
        ret = RunContainer.PruneContainer(id)
        retu = requests.delete("http://localhost:3000/docker", json={"name":ret[0]})
        print(ret)
        return ret
class ForcePruneContainer(Resource):
    def get(self,id):
        ret = RunContainer.ForcePruneContainer(id)
        retu = requests.delete("http://localhost:3000/docker", json={"name":id})
        print(ret)
        return ret


api.add_resource(CreateRandomContainer, '/')
api.add_resource(StopContainer, '/stop/<string:id>')
api.add_resource(PruneContainer, '/prune/<string:id>')
api.add_resource(ForcePruneContainer,'/fprune/<string:id>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)