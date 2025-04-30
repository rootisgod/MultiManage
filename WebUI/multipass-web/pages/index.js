import { useEffect, useState } from "react";
import axios from "axios";

// Component for displaying instance list with selection and start/stop functionality
function InstanceList({ instances, onRefresh, isRefreshing }) {
  const [selectedInstance, setSelectedInstance] = useState(null);
  const [actionInProgress, setActionInProgress] = useState(false);

  const handleRowClick = (instance) => {
    setSelectedInstance(selectedInstance?.name === instance.name ? null : instance);
  };

  const startInstance = () => {
    if (!selectedInstance) return;
    
    setActionInProgress(true);
    axios
      .post("http://localhost:8000/start", { name: selectedInstance.name })
      .then(() => {
        // After successful start, refresh the list to show updated state
        onRefresh();
      })
      .catch((error) => {
        console.error(`Error starting instance ${selectedInstance.name}:`, error);
      })
      .finally(() => {
        setActionInProgress(false);
      });
  };

  const stopInstance = () => {
    if (!selectedInstance) return;
    
    setActionInProgress(true);
    axios
      .post("http://localhost:8000/stop", { name: selectedInstance.name })
      .then(() => {
        // After successful stop, refresh the list to show updated state
        onRefresh();
      })
      .catch((error) => {
        console.error(`Error stopping instance ${selectedInstance.name}:`, error);
      })
      .finally(() => {
        setActionInProgress(false);
      });
  };

  // Check if the selected instance can be started (if it's stopped)
  const canStart = selectedInstance && selectedInstance.state.toLowerCase() !== "running";
  
  // Check if the selected instance can be stopped (if it's running)
  const canStop = selectedInstance && selectedInstance.state.toLowerCase() === "running";
  
  return (
    <div className="section">
      <div className="section-header">
        <h2>Multipass Instances</h2>
        <div className="action-buttons">
          <button 
            onClick={startInstance} 
            disabled={!canStart || actionInProgress || isRefreshing}
            className="action-button start-button"
          >
            Start
          </button>
          <button 
            onClick={stopInstance} 
            disabled={!canStop || actionInProgress || isRefreshing}
            className="action-button stop-button"
          >
            Stop
          </button>
          <button 
            onClick={onRefresh} 
            disabled={isRefreshing || actionInProgress} 
            className="refresh-button"
          >
            {isRefreshing ? "Refreshing..." : "Refresh"}
          </button>
        </div>
      </div>
      {instances.length > 0 ? (
        <table border="1" style={{ borderCollapse: "collapse" }} className="instance-table">
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
              <tr 
                key={index}
                onClick={() => handleRowClick(item)}
                className={selectedInstance?.name === item.name ? "selected-row" : ""}
              >
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
      {actionInProgress && <div className="action-status">Processing request...</div>}
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
            state: "Stopped",
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
        .action-buttons {
          display: flex;
          gap: 8px;
        }
        .refresh-button, .action-button {
          padding: 5px 12px;
          background-color: #f5f5f5;
          border: 1px solid #ddd;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
        }
        .start-button {
          background-color: #e6f7e6;
          border-color: #c3e6cb;
        }
        .start-button:hover:not(:disabled) {
          background-color: #d4edda;
        }
        .stop-button {
          background-color: #f7e6e6;
          border-color: #e6c3c3;
        }
        .stop-button:hover:not(:disabled) {
          background-color: #edd4d4;
        }
        .refresh-button:hover:not(:disabled) {
          background-color: #e5e5e5;
        }
        .refresh-button:disabled, .action-button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
        .instance-table tbody tr {
          cursor: pointer;
          transition: background-color 0.2s;
        }
        .instance-table tbody tr:hover {
          background-color: #f5f5f5;
        }
        .selected-row {
          background-color: #e6f0ff !important;
        }
        .action-status {
          margin-top: 10px;
          font-style: italic;
          color: #666;
        }
      `}</style>
    </div>
  );
}