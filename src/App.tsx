/*
Copyright (C) 2023 bkf2020

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { useState, useEffect } from 'react'

function App() {
  const [problemGroups, setProblemGroups] = useState<any[]>([]);
  const [origProblemGroups, setOrigProblemGroups] = useState<any[]>([]);
  const [elementsToUse, setElementsToUse] = useState(10);
  const [active, setActive] = useState("results1.0.json");
  function searchProblemGroups() {
    setElementsToUse(10);
    let regexStr = (document.getElementById("search") as HTMLInputElement).value;
    let empty = false;
    if(regexStr === null || regexStr === "") {
      regexStr = "[\\s\\S]";
      empty = true;
    }
    const regex = new RegExp(regexStr);
    var newProblemGroups = [];
    for(let key in origProblemGroups) {
      var found = false, currGroup = [];
      for(let i = 0; i < origProblemGroups[key].length; i++) {
        currGroup.push(origProblemGroups[key][i]);
        currGroup[i].highlight = false;
        if(regex.test(origProblemGroups[key][i].problem_name)) {
          if(!empty) {
            currGroup[i].highlight = true;
          }
          found = true;
        }
      }
      if(found) {
        newProblemGroups.push(currGroup);
      }
    }
    setProblemGroups(newProblemGroups);
  }
  function getProblemGroups(fileName : string) {
    setActive(fileName);
    fetch(fileName)
    .then(response => response.json())
    .then(function(dataJSON) {
      setOrigProblemGroups(dataJSON);
      setProblemGroups(dataJSON);
      setElementsToUse(10);
    });
  }
  function determineTheme() {
    if(!("theme" in localStorage)) {
      if(window.matchMedia("(prefers-color-scheme:dark)").matches) {
        localStorage.theme = "dark";
      } else {
        localStorage.theme = "light";
      }
    }
    document.documentElement.className = localStorage.theme;
  }
  function switchTheme() {
    if(!("theme" in localStorage)) {
      determineTheme();
    }
    if(localStorage.theme === "light") {
      localStorage.theme = "dark";
    } else {
      localStorage.theme = "light";
    }
    document.documentElement.className = localStorage.theme;
  }
  useEffect(() => {
    getProblemGroups("results1.0.json");
    determineTheme();
  }, []);
  function resetProblemGroups() {
    (document.getElementById("search") as HTMLInputElement).value = "";
    searchProblemGroups();
  }
  interface Threshold {
    fileName: string;
    num: string;
  }
  function ThresholdButton(props : Threshold) {
    if(active === props.fileName) {
      return <button className="bg-blue-300 hover:bg-blue-100 rounded p-2.5 text-black" onClick={() => getProblemGroups(props.fileName)}>{props.num}</button>;
    } else {
      return <button className="bg-green-300 hover:bg-green-100 rounded p-2.5 text-black" onClick={() => getProblemGroups(props.fileName)}>{props.num}</button>;
    }
  }

  return (
    <div className="App">
      <nav className="bg-blue-100 dark:bg-blue-700 border-2 border-blue-400 shadow dark:shadow-stone-400 px-2 rounded container flex items-center justify-between w-11/12 mx-auto max-w-screen-lg my-2.5">
        <p className="text-2xl text-blue-800 dark:text-blue-100">Ripples</p>
        <div className="flex gap-3 items-center">
          <button className="underline text-blue-600 dark:text-blue-200 hover:text-blue-800 dark:hover:text-blue-300" onClick={() => switchTheme()}>Switch theme</button>
          <span className="text-blue-800 dark:text-blue-100">|</span>
          <a href="https://github.com/bkf2020/ripples" target="_blank" rel="noopener noreferrer">Github</a>
        </div>
      </nav>
      <article className="dark:border-2 dark:border-teal-400 bg-[url('/patrick-connor-klopf-o4ahMT4wHH0-unsplash.jpg')] bg-no-repeat bg-cover bg-center shadow dark:shadow-stone-400 rounded p-2.5 w-11/12 mx-auto max-w-screen-lg my-2.5">
        <h2 className="text-xl text-green-100"><u>About Ripples</u></h2>
        <p className="text-white">
          An experimental tool using machine learning models (namely <a className="dark-a" href="https://github.com/UKPLab/sentence-transformers" target="_blank" rel="noopener noreferrer">sentence-transformers from UKPLab</a>)
          to try to determine <b>similar problems</b> from the <b>AMC 8/10/12 (American Mathematics Competitions)</b> and 
          <b> AIME (American Invitational Mathematics Examination)</b>.
          More information on <a className="dark-a" href="https://github.com/bkf2020/ripples" target="_blank" rel="noopener noreferrer">Github</a> and AoPS (ADD LATER).
        </p>
        <hr className='mt-3'/>
        <p className="text-white"><img src="https://counter.digits.net/?counter={40e68f8d-97d7-5244-c946-b7506b65b94c}&template=simple" alt="Hit Counter by Digits" className="inline"/> hit according to <a className="dark-a" href="http://www.digits.net/" target="_blank" rel="noopener noreferrer">Digits Web Counter</a></p>
      </article>
      <article className="bg-white dark:bg-stone-900 dark:text-stone-200 shadow-md dark:shadow-stone-400 rounded border-2 border-purple-400 p-2.5 w-11/12 mx-auto max-w-screen-lg my-2.5">
        <p>Select the threshold you want the model to have when classifying problems are similar. Higher numbers means the lower the barrier for problems to be similar.</p>
        <div className="flex gap-3 m-1">
          <ThresholdButton num="1.0" fileName="results1.0.json" />
          <ThresholdButton num="1.125" fileName="results1.125.json" />
          <ThresholdButton num="1.25" fileName="results1.25.json" />
          <ThresholdButton num="1.5" fileName="results1.5.json" />
        </div>
        <div className="flex flex-wrap gap-3 items-center justify-center m-4">
          <input id="search" type="search" className="border-2 border-blue-600 dark:border-blue-200 bg-gray-200 dark:bg-stone-600 block w-11/12 min-w-fit max-w-[700px] rounded p-2 h-10" placeholder="Search for a problem (regex supported)"></input>
          <div>
            <button className="bg-blue-300 hover:bg-blue-100 rounded mr-3 p-2.5 text-black max-h-11" onClick={() => searchProblemGroups()}>Search</button>
            <button className="bg-teal-300 hover:bg-teal-100 rounded p-2.5 text-black max-h-11" onClick={() => resetProblemGroups()}>Reset</button>
          </div>
        </div>
        <center><p className="text-sm"><b>Note:</b> you will have to press the search button again after changing the threshold value.</p></center>
        <table className="table-auto my-2.5">
          <tbody className="[&>*:nth-child(even)]:bg-red-100 [&>*:nth-child(even)]:dark:bg-slate-700">
            <tr><th>Similar problems</th></tr>
            {
              Object.keys(problemGroups).slice(0, elementsToUse).map((key: any, cnt) => (
                <tr className="border-2 border-stone-900 dark:border-stone-100"><td className="p-1.5 flex flex-wrap gap-2">
                  {
                    Object.keys(problemGroups[key]).map((i) => {
                      if(problemGroups[key][i].highlight) {
                        return <a className="min-w-fit rounded border bg-yellow-100 dark:bg-yellow-900 dark:text-stone-300 border-gray-700 dark:border-gray-100 m-2 p-1 no-underline" href={problemGroups[key][i].problem_link} target="_blank" rel="noopener noreferrer">{problemGroups[key][i].problem_name}</a>
                      } else {
                        return <a className="min-w-fit rounded border dark:text-stone-300 border-gray-700 dark:border-gray-100 m-2 p-1 no-underline" href={problemGroups[key][i].problem_link} target="_blank" rel="noopener noreferrer">{problemGroups[key][i].problem_name}</a>
                      }
                    })
                  }
                </td></tr>
              ))
            }
          </tbody>
        </table>
        <button className="bg-orange-300 rounded p-1.5 text-black" onClick={() => setElementsToUse(elementsToUse + 10)}>Show more</button>
      </article>
    </div>
  )
}

export default App
