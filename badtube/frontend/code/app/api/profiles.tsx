import type { Movie } from "./movies";

export interface Profile {
    id: string
    email?: string
    username: string,
    firstname: string,
    lastname: string,
    language: string,
    profile_picture: string
}

export function get_formated_title(m: Movie): string {
    return m.release_date != null ? m.title + ` (${m.release_date})` : m.title;
}