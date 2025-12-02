export default function Component() {
    return (
        <div className="bg-violet-300">
            <form className="flex gap-2">
                <button type="submit">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-8">
                        <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
                    </svg>
                </button>
                <input placeholder="search a movie name :)" className="bg-gray-300 flex-1" type="text" required name="name"></input>
            </form>
        </div>
    );
}