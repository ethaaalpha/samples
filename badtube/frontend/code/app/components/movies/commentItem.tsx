import type { MovieComment } from "~/api/comments";

interface CommentProps {
    comment: MovieComment
}

export default function Component({comment}: CommentProps) {
    return (
        <div className="bg-amber-400">
            <div className="flex items-center gap-2">
                <p className="font-bold text-lg">{comment.username}</p>
                <p className="font-light italic">{comment.date}</p>
            </div>
            <p>{comment.content}</p>
        </div>
    );
}
