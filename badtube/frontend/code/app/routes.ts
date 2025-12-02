import { type RouteConfig, index, layout, prefix, route } from "@react-router/dev/routes";

export default [
    index("routes/index.tsx"),

    layout("layouts/principal.tsx", [
        ...prefix("movies", [
            index("routes/movies/index.tsx"),
            route(":movieId", "routes/movies/movie.tsx")
        ]),
        ...prefix("profiles", [
            index("routes/profiles/index.tsx"),
            route(":profileId", "routes/profiles/profile.tsx")
        ])
    ])
] satisfies RouteConfig;
