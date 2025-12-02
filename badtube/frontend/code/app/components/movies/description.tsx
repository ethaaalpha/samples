import type { Movie } from "~/api/movies";
import { get_formated_title } from "~/api/profiles";

interface MovieProps {
    movie: Movie
}

export default function Component({movie}: MovieProps) {
    let directorComponent = null;
    let actorsComponent = null;

    if (movie.director) {
        directorComponent = (
            <p>Director: {movie.director}</p>
        );
    }
    if (movie.actors.length > 0) {
        actorsComponent = (
            <p>Casting: {movie.actors.join(", ")}</p>
        );
    }

    return (
        <div className="bg-fuchsia-300">
            <p className="font-bold text-3xl">{get_formated_title(movie)}</p>
            <p className="italic font-medium">{movie.duration} minutes</p>
            <p>Rating: {movie.rating}</p>
            <p className="italic">{movie.desc}</p>
            {directorComponent}
            {actorsComponent}
        </div>
    );
}