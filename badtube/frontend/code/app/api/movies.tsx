import type { Route } from "../+types/root"
import { get_url } from "./tools"

export interface Movie {
    id: string,
    title: string,
    rating: string,
    img_link: string
    release_date?: Date,
    duration: number
    actors: string[]
    director?: string
    desc: string
}

export interface MovieResult {
    movie: Movie
    seen: boolean
}

export async function get_movies(name: string | null, page: number): Promise<MovieResult[]> {
    if (page < 0) {
        page = 1;
    }

    const optional = name ? `&name=${name}` : ""
    const res = await fetch(get_url(`/movies?page=${page}${optional}`));

    return await res.json();
}
