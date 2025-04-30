import { useEffect, useState } from "react";
import axios from "axios";

export default function Home() {
  const [multipassVersion, setMultipassVersion] = useState([]);
  const [multipassList, setMultipassList] = useState([]);
  const isDebugMode = false; // Toggle to true for debugging, false for production

  useEffect(() => {
    if (isDebugMode) {
      // Test data mimicking the FastAPI JSON response
      const testInstanceListData = {
        list: [
          {
            ipv4: [],
            name: "beloved-burro",
            release: "Ubuntu 24.04 LTS",
            state: "Deleted",
          },
          {
            ipv4: ["192.168.1.100", "192.168.1.101"],
            name: "happy-llama",
            release: "Ubuntu 22.04 LTS",
            state: "Running",
          },
        ],
      };
      const testMultipassVersionData = {
        version: {
          "multipass": "1.15.1+mac",
          "multipassd": "1.15.1+mac"
        }
      };
      setMultipassList(testInstanceListData.list);
      setMultipassVersion(testMultipassVersionData); // Example version
    } else {
      // Fetch data from the FastAPI endpoint
      axios
        .get("http://localhost:8000/list")
        .then((response) => {
          // Assuming the response.data is the JSON object with a "list" key
          setMultipassList(response.data.list);
        })
        .catch((error) => {
          console.error("Error fetching multipass list:", error);
        });
      // Fetch Multipass Version
      axios
      .get("http://localhost:8000/version")
      .then((response) => {
        // Assuming the response.data is the JSON object with a "list" key
        setMultipassVersion(response.data);
      })
      .catch((error) => {
        console.error("Error fetching multipass version:", error);
      });
    }
  }, []);

  return (
    <div>
      <h1>Multipass Instances (Version: multipass {multipassVersion.multipass}, multipassd {multipassVersion.multipassd})</h1>
      {multipassList.length > 0 ? (
        <table border="1" style={{ borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ padding: "8px" }}>Name</th>
              <th style={{ padding: "8px" }}>Release</th>
              <th style={{ padding: "8px" }}>State</th>
              <th style={{ padding: "8px" }}>IPv4</th>
            </tr>
          </thead>
          <tbody>
            {multipassList.map((item, index) => (
              <tr key={index}>
                <td style={{ padding: "8px" }}>{item.name}</td>
                <td style={{ padding: "8px" }}>{item.release}</td>
                <td style={{ padding: "8px" }}>{item.state}</td>
                <td style={{ padding: "8px" }}>
                  {item.ipv4.length > 0 ? item.ipv4.join(", ") : "None"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No instances found.</p>
      )}
    </div>
  );
}