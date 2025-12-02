import { Navigate } from "react-router";
import Footer from "~/components/footer";
import Header from "~/components/header";

export default function Home() {
    return <Navigate to="/movies" replace />;
}
