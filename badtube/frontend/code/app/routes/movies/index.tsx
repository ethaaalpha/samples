import { use, useEffect, useRef, useState } from "react";
import { get_movies, type Movie, type MovieResult } from "~/api/movies";
import Thumbmail from "~/components/movies/thumbmail";
import type { Route } from "./+types";
import Search from "~/components/movies/search";
import { useFetcher } from "react-router";

const SIZE = 6

// when the route is loading (after it will be useState & handleScroll)
export async function clientLoader({ request }: Route.ClientLoaderArgs) {
    const url = new URL(request.url)

    return await get_movies(url.searchParams.get("name"), 1);
}

export default function Component({loaderData}: Route.ComponentProps) {
    const [moviesCache, setMoviesCache] = useState<MovieResult[]>(loaderData);
    const [movies, setMovies] = useState<MovieResult[]>([]);
    const [page, setPage] = useState<number>(1);
    const [endData, setEndData] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    const pullCache = (): MovieResult[] => {
        let chunk: MovieResult[] = [];

        setMoviesCache(prev => {
            chunk = prev.slice(0, SIZE);
            return prev.slice(SIZE);
        });

        return chunk;
    };

    const updateMovies = () => {
        const nextData = pullCache();

        if (nextData.length == 0) {
            setEndData(true);
        } else {
            setMovies(prev => [...prev, ...nextData]);
        }
    }

    const handleScroll = () => {
        const item = scrollRef.current;
        console.log("PAR LA")

        if (endData || ! item || loading) {
            console.log("ICI " + endData + " " + loading)
            return;
        }

        if (item.scrollTop + item.clientHeight >= item.scrollHeight - 50) {
            setLoading(true);
            updateMovies()
            setLoading(false);
        }
    }

    useEffect(() => {
        updateMovies();
    }, []);

    return (
        <div ref={scrollRef} onScroll={handleScroll} className="h-screen overflow-y-auto">
            <Search/>
            <div className="grid grid-cols-2 gap-10 justify-items-center">
                {movies.map((data) => (
                <Thumbmail key={data.movie.id} movie={data.movie} seen={data.seen} />
            ))}
            </div>
        </div>
    );
}



    // const pullCache = (): MovieResult[] => {
    //     const data = moviesCache.slice(0, SIZE);
    //     setMoviesCache(prev => [...prev.slice(SIZE)])

    //     // prepare some cache
    //     // if (moviesCache.length < SIZE) {
    //     //     const toCache = await get_movies(null, page + 1);

    //     //     console.log("TO CACHE " + toCache)
    //     //     setPage(prev => prev + 1);
    //     //     setMoviesCache(prev => [...prev, ...toCache]);
    //     // }
    //     return data;
    // }