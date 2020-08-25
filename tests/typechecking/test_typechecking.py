import validx as v


city_schema: v.Validator = v.Dict(
    {
        "location": v.Tuple(v.Float(min=-90, max=90), v.Float(min=-180, max=180)),
        "name": v.Str(),
        "alt_names": v.List(v.Str(), unique=True),
        "population": v.Dict({"city": v.Int(min=0), "metro": v.Int(min=0)}),
    },
    extra=(v.Str(), v.Any()),
)
