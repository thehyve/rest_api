import json
import time
from flask import current_app
from flask.ext import restful
from flask.ext.restful import abort
from app.common.auth import is_authenticated
from app.common.rate_limit import rate_limit
from app.common.response_templates import CTTVResponse
from app.common.results import RawResult


class TargetInfo(restful.Resource):

    @is_authenticated
    @rate_limit
    def get(self, target_id ):
        '''
        Get target generic information from an ensembl gene id'''
        start_time = time.time()
        es = current_app.extensions['esquery']
        res = es.get_gene_info([target_id])
        if res:
            data = res.toDict()['data']
            if data:
                return CTTVResponse.OK(RawResult(json.dumps(data[0])), took=time.time() - start_time)

        abort(404, message="Gene id %s cannot be found"%target_id)

