import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Form from "./Form";
import MusicList from "./MusicList";
import Test from "./Test";
import Layout from "./shared/Layout";
function App() {
  return (
    <Router>
        <Routes>
            <Route exact path='/' element={<Layout/>}>
                <Route index element={<Form/>} />
                <Route path='/desc' element={<Form/>} />
                <Route path='/test' element={<Test/>} />
            </Route>
        </Routes>
    </Router>
  );
}

export default App;
