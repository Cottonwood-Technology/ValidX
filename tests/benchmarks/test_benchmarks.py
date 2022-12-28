"""
Competitors

1.  ValidX (Python version)
2.  ValidX (Cython version)
3.  Cerberus: http://docs.python-cerberus.org/en/stable/
4.  Colander: https://docs.pylonsproject.org/projects/colander/en/latest/
5.  JSONSchema: https://python-jsonschema.readthedocs.io/en/latest/
6.  Schema: https://github.com/keleshev/schema
7.  Valideer: https://github.com/podio/valideer
8.  Voluptuous: http://alecthomas.github.io/voluptuous/docs/_build/html/index.html
9.  Validr: https://github.com/guyskk/validr
10. Marshmallow: https://marshmallow.readthedocs.io/en/stable/

"""


data = {
    "location": {"lat": 50.046_428_4, "lng": 19.724_694_2},
    "name": "Kraków",
    "alt_names": ["Krakow", "Cracow"],
    "population": {"city": 766_739, "metro": 1_725_894},
}


def test_validx_py(benchmark):
    from validx.py import Dict, List, Str, Float, Int

    schema = Dict(
        {
            "location": Dict(
                {"lat": Float(min=-90, max=90), "lng": Float(min=-180, max=180)}
            ),
            "name": Str(),
            "alt_names": List(Str()),
            "population": Dict({"city": Int(min=0), "metro": Int(min=0)}),
        }
    )
    assert benchmark(schema, data) == data


def test_validx_cy(benchmark):
    from validx.cy import Dict, List, Str, Float, Int

    schema = Dict(
        {
            "location": Dict(
                {"lat": Float(min=-90, max=90), "lng": Float(min=-180, max=180)}
            ),
            "name": Str(),
            "alt_names": List(Str()),
            "population": Dict({"city": Int(min=0), "metro": Int(min=0)}),
        }
    )
    assert benchmark(schema, data) == data


def test_cerberus(benchmark):
    from cerberus import Validator

    schema = Validator(
        {
            "location": {
                "type": "dict",
                "schema": {
                    "lat": {"type": "float", "min": -90, "max": 90},
                    "lng": {"type": "float", "min": -180, "max": 180},
                },
            },
            "name": {"type": "string"},
            "alt_names": {"type": "list", "schema": {"type": "string"}},
            "population": {
                "type": "dict",
                "schema": {
                    "city": {"type": "integer", "min": 0},
                    "metro": {"type": "integer", "min": 0},
                },
            },
        }
    )
    assert benchmark(schema, data)


def test_colander(benchmark):
    import colander as c

    class Point(c.MappingSchema):
        lat = c.SchemaNode(c.Float(), validator=c.Range(-90, 90))
        lng = c.SchemaNode(c.Float(), validator=c.Range(-180, 180))

    class Names(c.SequenceSchema):
        name = c.SchemaNode(c.String())

    class Population(c.MappingSchema):
        city = c.SchemaNode(c.Int(), validator=c.Range(min=0))
        metro = c.SchemaNode(c.Int(), validator=c.Range(min=0))

    class City(c.MappingSchema):
        location = Point()
        name = c.SchemaNode(c.String())
        alt_names = Names()
        population = Population()

    schema = City()
    assert benchmark(schema.deserialize, data) == data


def test_jsonschema(benchmark):
    from jsonschema import Draft202012Validator

    schema = Draft202012Validator(
        {
            "type": "object",
            "properties": {
                "location": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "number", "minimum": -90, "maximum": 90},
                        "lng": {"type": "number", "minimum": -180, "maximum": 180},
                    },
                },
                "name": {"type": "string"},
                "alt_names": {"type": "array", "items": {"type": "string"}},
                "population": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "number", "minimum": 0},
                        "metro": {"type": "number", "minimum": 0},
                    },
                },
            },
        },
    )
    assert benchmark(schema.validate, data) is None


def test_schema(benchmark):
    from schema import Schema, And

    schema = Schema(
        {
            "location": {
                "lat": And(float, lambda x: -90 <= x <= 90),
                "lng": And(float, lambda x: -180 <= x <= 180),
            },
            "name": str,
            "alt_names": [str],
            "population": {
                "city": And(int, lambda x: x >= 0),
                "metro": And(int, lambda x: x >= 0),
            },
        }
    )
    assert benchmark(schema.validate, data) == data


def test_valideer(benchmark):
    import valideer

    schema = valideer.parse(
        {
            "+location": {
                "+lat": valideer.Range("number", min_value=-90, max_value=90),
                "+lng": valideer.Range("number", min_value=-180, max_value=180),
            },
            "+name": "string",
            "+alt_names": ["string"],
            "+population": {
                "+city": valideer.Range("number", min_value=0),
                "+metro": valideer.Range("number", min_value=0),
            },
        }
    )
    assert benchmark(schema.is_valid, data) is True


def test_voluptuous(benchmark):
    from voluptuous import Schema, All, Range

    schema = Schema(
        {
            "location": {
                "lat": All(float, Range(min=-90, max=90)),
                "lng": All(float, Range(min=-180, max=180)),
            },
            "name": str,
            "alt_names": [str],
            "population": {
                "city": All(int, Range(min=0)),
                "metro": All(int, Range(min=0)),
            },
        }
    )
    assert benchmark(schema, data) == data


def test_validr(benchmark):
    from validr import T, Compiler

    schema = Compiler().compile(
        T.dict(
            location=T.dict(
                lat=T.float.min(-90).max(90), lng=T.float.min(-180).max(180)
            ),
            name=T.str,
            alt_names=T.list(T.str),
            population=T.dict(city=T.int.min(0), metro=T.int.min(0)),
        )
    )
    assert benchmark(schema, data) == data


def test_marshmallow(benchmark):
    import marshmallow as m

    class Point(m.Schema):
        lat = m.fields.Float(validate=m.validate.Range(-90, 90))
        lng = m.fields.Float(validate=m.validate.Range(-180, 180))

    class Names(m.Schema):
        name = m.fields.Str()

    class Population(m.Schema):
        city = m.fields.Int(validate=m.validate.Range(min=0))
        metro = m.fields.Int(validate=m.validate.Range(min=0))

    class City(m.Schema):
        location = m.fields.Nested(Point())
        name = m.fields.Str()
        alt_names = m.fields.List(m.fields.Str())
        population = m.fields.Nested(Population())

    schema = City()
    assert benchmark(schema.validate, data) == {}
