export default function Component() {
    return (
        <div className="bg-emerald-300">
            <form>
                <label htmlFor="content">Write a comment?</label>
                <div className="flex flex-row">
                    <input className="bg-white flex-1" type="text" required name="content"></input>
                    <button type="submit" className="bg-amber-50">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
                        </svg>
                    </button>
                </div>
            </form>
        </div>
    );
}