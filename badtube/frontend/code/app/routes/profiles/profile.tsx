import Profile from "~/components/profiles/profile";

export default function Component() {
    const p: typeof Profile = {
        id: "terst",
        username: "example",
        firstname: "Michel",
        lastname: "example",
        email: "magiceverywhere@gmail.com",
        profile_picture: "https://media.sproutsocial.com/uploads/2022/06/profile-picture.jpeg",
        language: "FR"
    };

    return (
        <Profile profile={p} editable={false}/>
    );
}