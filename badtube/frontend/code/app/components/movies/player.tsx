interface PlayerProps {
    url: string
}

export default function Component({url}: PlayerProps) {
    return (
        <video controls className="w-full">
            <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4" />
        </video>
    );
}