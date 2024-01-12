import {Link} from "react-router-dom";
import {useLocation} from 'react-router-dom';


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

export default function Test(state) {
    const location = useLocation();
    var songs = location.state.songs
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