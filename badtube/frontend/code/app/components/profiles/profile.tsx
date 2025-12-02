import type { Profile } from "~/api/profiles";

interface ProfileProps {
    profile: Profile,
    editable: boolean
}

export default function Component({profile, editable}: ProfileProps) {
    let imgComponent = null;
    let langComponent = null;

    if (editable) {
        imgComponent = (
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-10 absolute inset-0 m-auto">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5" />
            </svg>
        )
        langComponent = (
            <select>
                <option>FR</option>
                <option>EN</option>
            </select>
        );
    } else {
        langComponent = <p>{profile.language}</p>
    }

    return (
        <div className="flex flex-col pt-5">
            <div className="relative justify-items-center">
                {imgComponent}
                <img className="w-70 h-70 rounded-full object-cover justify-items-center" src={profile.profile_picture}></img>
            </div>
            <div className="flex flex-col items-center pt-10 text-2xl">
                <p className="font-bold">{profile.username}</p>
                <p>{profile.email}</p>
                <p>{profile.firstname} {profile.lastname}</p>
                {langComponent}
            </div>
        </div>
    );
}