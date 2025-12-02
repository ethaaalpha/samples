import { Outlet } from "react-router";
import Footer from "~/components/footer";
import Header from "~/components/header"

export default function Component() {
    return (
        <div className="flex flex-col min-h-screen">
            <Header/>
            <main className="flex-1 wrap-anywhere">
                <Outlet/>
            </main>
            <Footer/>
        </div>
    );
}