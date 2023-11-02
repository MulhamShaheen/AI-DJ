import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Form from "./Form";
import MusicList from "./MusicList";
import Layout from "./shared/Layout";
function App() {
  return (
    <Router>
        <Routes>
            <Route exact path='/' element={<Layout/>}>
                <Route index element={<MusicList/>} />
                <Route path='/desc' element={<Form/>} />
            </Route>
        </Routes>
    </Router>
  );
}

export default App;
