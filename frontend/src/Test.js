import {Link} from "react-router-dom";
import {useState} from "react";
import axios from "axios";
import {SONG_LIST_URL} from "./index";


function ListItem({title, artist, popularity}) {
    return (
        <li className="py-3 sm:py-4">
            <div className="flex items-center space-x-4">

                <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate dark:text-white">{title}</p>
                    <p className="text-sm text-gray-500 truncate dark:text-gray-400">{artist}</p>
                </div>
                <div className="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                    {popularity}
                </div>
            </div>
        </li>
    );
}

export default function Test() {

    const [songs, setSongs] = useState([])

    axios.get(SONG_LIST_URL).then(data => setSongs(data.data))
    return (
        <div >
            <ul className="max-w-screen-xl divide-y divide-gray-200 dark:divide-gray-700">
                {songs.map((item, index) => (
                    <ListItem key={index} {...item} />
                ))}
            </ul>
        </div>
    );
}