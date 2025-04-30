import { useEffect, useState } from "react";
import axios from "axios";

// Component for displaying instance list
function InstanceList({ instances, onRefresh, isRefreshing }) {
  return (
    <div className="section">
      <div className="section-header">
        <h2>Multipass Instances</h2>
        <button 
          onClick={onRefresh} 
          disabled={isRefreshing} 
          className="refresh-button"
        >
          {isRefreshing ? "Refreshing..." : "Refresh"}
        </button>
      </div>
      {instances.length > 0 ? (
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
            {instances.map((item, index) => (
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

// Component for displaying version info
function VersionInfo({ version }) {
  return (
    <div className="section">
      <h2>Multipass Version</h2>
      <p>
        multipass: {version.multipass || 'Unknown'}<br />
        multipassd: {version.multipassd || 'Unknown'}
      </p>
    </div>
  );
}

// You can add more components for other API sections here
// For example: InstanceStats, NetworkInfo, etc.

export default function Home() {
  const [multipassVersion, setMultipassVersion] = useState({});
  const [multipassList, setMultipassList] = useState([]);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const isDebugMode = false; // Toggle to true for debugging, false for production

  // Function to fetch instance list
  const fetchInstanceList = () => {
    setIsRefreshing(true);
    axios
      .get("http://localhost:8000/list")
      .then((response) => {
        setMultipassList(response.data.list);
      })
      .catch((error) => {
        console.error("Error fetching multipass list:", error);
      })
      .finally(() => {
        setIsRefreshing(false);
      });
  };

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
      setMultipassVersion(testMultipassVersionData.version); 
    } else {
      // Fetch initial data
      fetchInstanceList();
      
      // Fetch Multipass Version
      axios
        .get("http://localhost:8000/version")
        .then((response) => {
          setMultipassVersion(response.data.version || {});
        })
        .catch((error) => {
          console.error("Error fetching multipass version:", error);
        });
        
      // You can add more API calls here as needed
    }
  }, []);

  return (
    <div className="container">
      <h1>Multipass Manager</h1>
      
      {/* Main content sections */}
      <div className="sections">
        <VersionInfo version={multipassVersion} />
        <InstanceList 
          instances={multipassList} 
          onRefresh={fetchInstanceList}
          isRefreshing={isRefreshing}
        />
        
        {/* You can add more sections here */}
        {/* <OtherSection data={otherData} /> */}
      </div>
      
      {/* Optional: Add some basic styling */}
      <style jsx>{`
        .container {
          padding: 20px;
          max-width: 1200px;
          margin: 0 auto;
        }
        .sections {
          display: flex;
          flex-direction: column;
          gap: 30px;
        }
        .section {
          padding: 15px;
          border: 1px solid #eaeaea;
          border-radius: 5px;
        }
        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;
        }
        .refresh-button {
          padding: 5px 12px;
          background-color: #f5f5f5;
          border: 1px solid #ddd;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
        }
        .refresh-button:hover {
          background-color: #e5e5e5;
        }
        .refresh-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
}