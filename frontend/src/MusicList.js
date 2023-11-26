import React from 'react';


const topMusicTracks = [
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 1',
        musicName: 'Music 1',
        time: '3:30',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 2',
        musicName: 'Music 2',
        time: '4:15',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 3',
        musicName: 'Music 3',
        time: '2:45',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 4',
        musicName: 'Music 4',
        time: '3:50',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 5',
        musicName: 'Music 5',
        time: '3:10',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 6',
        musicName: 'Music 6',
        time: '4:05',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 7',
        musicName: 'Music 7',
        time: '3:15',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 8',
        musicName: 'Music 8',
        time: '2:55',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 9',
        musicName: 'Music 9',
        time: '4:30',
    },
    {
        imageSrc: 'https://images.8tracks.com/cover/i/009/963/681/music-8230.jpg?rect=0,0,2400,2400&q=98&fm=jpg&fit=max',
        artistName: 'Artist 10',
        musicName: 'Music 10',
        time: '3:20',
    },
];


function ListItem({ imageSrc, artistName, musicName, time }) {
    return (
        <li className="py-3 sm:py-4">
            <div className="flex items-center space-x-4">
                <div className="flex-shrink-0">
                    <img className="w-8 h-8 rounded-full" src={imageSrc} alt={`${artistName} image`} />
                </div>
                <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate dark:text-white">{artistName}</p>
                    <p className="text-sm text-gray-500 truncate dark:text-gray-400">{musicName}</p>
                </div>
                <div className="inline-flex items-center text-base font-semibold text-gray-900 dark:text-white">
                    {time}
                </div>
            </div>
        </li>
    );
}

function MusicList() {
    return (
        <div >
            <ul className="max-w-screen-xl divide-y divide-gray-200 dark:divide-gray-700">
                {topMusicTracks.map((item, index) => (
                    <ListItem key={index} {...item} />
                ))}
            </ul>
        </div>
    );
}

export default MusicList;
