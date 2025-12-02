import type { Movie } from "~/api/movies";
import { get_formated_title } from "~/api/profiles";

interface MovieProps {
    movie: Movie
    seen: boolean
}

export default function Component({movie, seen} : MovieProps) {
    const title = get_formated_title(movie);
    const color = seen ? "bg-red-500" : "bg-emerald-500 " 

    return (
        <div className={`${color} p-1`}>
            <div className="flex flex-col relative">
                <div className="absolute right-0 p-1 bg-blue-400">
                    <p className="">{movie.rating}</p>
                </div>
                <img src={movie.img_link}></img>
                <p className="text-center">{title}</p>
            </div>
        </div>
    );
}