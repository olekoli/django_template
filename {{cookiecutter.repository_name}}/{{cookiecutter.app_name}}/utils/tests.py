import json
from typing import Dict

from graphene_django.utils import GraphQLTestCase
from django.http import HttpResponse
from rest_framework.test import APIClient

from ..users.models import User

# from django_template.schema import schema


class ExtendedGraphQLTestCase(GraphQLTestCase):

    # GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = "/graphql/"

    @classmethod
    def setUpClass(cls):
        super(ExtendedGraphQLTestCase, cls).setUpClass()

        if not cls.GRAPHQL_SCHEMA:
            raise AttributeError(
                "Variable GRAPHQL_SCHEMA not defined in GraphQLTestCase."
            )

        cls._client = APIClient()

    @staticmethod
    def _build_query(query: str, op_name: str = None, input_data: dict = None) -> Dict:
        body = {"query": query}
        if op_name:
            body["operation_name"] = op_name
        if input_data:
            body["variables"] = input_data
        return json.dumps(body)

    def authenticated_query(
        self,
        user: User,
        query: str,
        op_name: str = None,
        input_data: dict = None,
        check_for_errors: bool = True,
    ) -> HttpResponse:
        local_client = self._client
        local_client.force_authenticate(user)
        body = self._build_query(query, op_name, input_data)
        resp = local_client.post(
            self.GRAPHQL_URL, data=body, content_type="application/json"
        )
        if check_for_errors:
            self.assertResponseNoErrors(resp)
        return resp

    def assertDictValuesEqual(self, first: Dict, second: Dict) -> None:
        self.assertEqual(list(first.values()), list(second.values()))
