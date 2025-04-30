import { useEffect, useState } from "react";
import axios from "axios";

export default function Home() {
  const [multipassList, setMultipassList] = useState([]);

  useEffect(() => {
    // Fetch data from the FastAPI endpoint
    axios.get("http://localhost:8000/list")
      .then((response) => {
        setMultipassList(response.data.output.split("\n")); // Assuming output is a newline-separated string
      })
      .catch((error) => {
        console.error("Error fetching multipass list:", error);
      });
  }, []);

  return (
    <div>
      <h1>Multipass Instances</h1>
      <ul>
        {multipassList.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}