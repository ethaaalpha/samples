import Profile from "~/components/profiles/profile";

export default function Component() {
    const p: typeof Profile = {
        id: "terst",
        username: "example",
        firstname: "Example",
        lastname: "Example",
        email: "magiceverywhere@gmail.com",
        profile_picture: "https://media.sproutsocial.com/uploads/2022/06/profile-picture.jpeg",
        language: "FR"
    };

    return (
        <Profile profile={p} editable={true}/>
    );
}