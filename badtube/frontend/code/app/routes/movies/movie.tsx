import type { Movie } from "~/api/movies";
import type { Route } from "./+types";
import Description from "~/components/movies/description";
import type { MovieComment } from "~/api/comments";
import CommentItem from "~/components/movies/commentItem";
import CommentForm from "~/components/movies/commentForm";
import Player from "~/components/movies/player";

export default function Component({params}: Route.ComponentProps) {
    const movie: Movie = {
        id: "123",
        title: "Zootopie",
        rating: "8.8",
        picture: "https://www.themoviedb.org/t/p/w1280/qq6MfHFDvBEzHhkE0Q5ozbkbde4.jpg",
        release_year: "2016",
        duration: 10,
        actors: ["Example Example", "Example Example"],
        director: "Super Gars",
        desc: "superdescription dudjhiwq o pdjiwqodjiw qpdjiqwpdj qwipdj qwipdjwq ipdj. wqipdjqwipdjwqidqwjipdwqjidpqwjidwqjipdqw"
    };

    const comment: MovieComment = {
        user_id: "321321",
        username: "supergeek",
        date: new Date(Date.now()).toLocaleDateString("fr-FR"),
        content: "je trouve ce film vraiment formidable, j'aimerais venir le revoir. Example Example danse vraiment tres bien dedans c'est fou"
    }

    return (
        <div className="flex flex-col gap-5">
            <Player url="test"/>
            <Description movie={movie}/>
            <CommentForm/>
            <CommentItem comment={comment}/>
            <CommentItem comment={comment}/>
        </div>
    );
}

