import {Outlet} from "react-router-dom";
import Footer from "./Footer";
import Navbar from "./Navbar";

export default function Layout() {
    return (
        <div className='bg-white rounded-lg shadow max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4'>
            <div className="w-full max-w-screen-lg p-4">
            <Navbar />
                <div className="pb-4"></div>
            <div className="bg-white p-4 rounded shadow-md">
                <div className="pb-4"></div>
                <Outlet/>
                <div className="pb-4"></div>
            </div>
                <div className="pb-4"></div>
            <Footer />
            </div>
        </div>
    )
}