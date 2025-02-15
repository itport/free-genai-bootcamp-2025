// @ts-nocheck
/* eslint-disable no-unused-vars */
/* eslint-disable react/prop-types */
/* eslint-disable react/no-unknown-property */
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useParams } from 'react-router-dom';

const API_BASE_URL = 'http://localhost:5000'; // Replace with your Flask backend URL

// --- Utility Functions ---
async function fetchData(url: string, options = {}) {
  const response = await fetch(`${API_BASE_URL}${url}`, options);
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'An error occurred');
  }
  return await response.json();
}

// --- Components ---

// --- Dashboard ---
function Dashboard() {
  const [recentSession, setRecentSession] = useState(null);
  const [stats, setStats] = useState(null);
  const [error, setError] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const recentSessionData = await fetchData('/dashboard/recent-session');
                setRecentSession(recentSessionData);

                const statsData = await fetchData('/dashboard/stats');
                setStats(statsData);
            } catch (err) {
                setError(err.message);
            }
        };
        loadData();
    }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Dashboard</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded shadow">
                    <h2 className="text-xl font-semibold mb-2">Recent Session</h2>
                    {recentSession ? (
                        <div>
                            <p>Activity: {recentSession.activity_name}</p>
                            <p>Created At: {new Date(recentSession.created_at).toLocaleString()}</p>
                            <p>Correct: {recentSession.correct_count}</p>
                            <p>Wrong: {recentSession.wrong_count}</p>
                        </div>
                    ) : (
                        <p>No recent session.</p>
                    )}
                </div>

                <div className="bg-white p-4 rounded shadow">
                    <h2 className="text-xl font-semibold mb-2">Study Stats</h2>
                    {stats ? (
                        <div>
                            <p>Total Vocabulary: {stats.total_vocabulary}</p>
                            <p>Words Studied: {stats.total_words_studied}</p>
                            <p>Mastered Words: {stats.mastered_words}</p>
                            <p>Success Rate: {(stats.success_rate * 100).toFixed(2)}%</p>
                            <p>Total Sessions: {stats.total_sessions}</p>
                            <p>Active Groups: {stats.active_groups}</p>
                            <p>Current Streak: {stats.current_streak}</p>
                        </div>
                    ) : (
                        <p>Loading stats...</p>
                    )}
                </div>
            </div>
        </div>
    );
}

// --- Words ---
function WordList() {
  const [words, setWords] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sortBy, setSortBy] = useState('kanji');
  const [order, setOrder] = useState('asc');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWords = async () => {
      try {
        const data = await fetchData(`/words?page=${currentPage}&sort_by=${sortBy}&order=${order}`);
        setWords(data.words);
        setTotalPages(data.total_pages);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchWords();
  }, [currentPage, sortBy, order]);

  const handleSort = (column) => {
    if (sortBy === column) {
      setOrder(order === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setOrder('asc');
    }
  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Word List</h1>
      <table className="min-w-full bg-white border border-gray-300">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b cursor-pointer" onClick={() => handleSort('kanji')}>Kanji</th>
            <th className="py-2 px-4 border-b cursor-pointer" onClick={() => handleSort('romaji')}>Romaji</th>
            <th className="py-2 px-4 border-b cursor-pointer" onClick={() => handleSort('english')}>English</th>
            <th className="py-2 px-4 border-b cursor-pointer" onClick={() => handleSort('correct_count')}>Correct</th>
            <th className="py-2 px-4 border-b cursor-pointer" onClick={() => handleSort('wrong_count')}>Wrong</th>
          </tr>
        </thead>
        <tbody>
          {words.map((word) => (
            <tr key={word.id}>
              <td className="py-2 px-4 border-b"><Link to={`/words/${word.id}`} className="text-blue-500 hover:underline">{word.kanji}</Link></td>
              <td className="py-2 px-4 border-b">{word.romaji}</td>
              <td className="py-2 px-4 border-b">{word.english}</td>
              <td className="py-2 px-4 border-b">{word.correct_count}</td>
              <td className="py-2 px-4 border-b">{word.wrong_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4 flex justify-between">
        <button
          onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
          disabled={currentPage === 1}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
        >
          Previous
        </button>
        <span>Page {currentPage} of {totalPages}</span>
        <button
          onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
          disabled={currentPage === totalPages}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-400"
        >
          Next
        </button>
      </div>
    </div>
  );
}

function WordDetail() {
  const { word_id } = useParams();
  const [word, setWord] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWord = async () => {
      try {
        const data = await fetchData(`/words/${word_id}`);
        setWord(data.word);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchWord();
  }, [word_id]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!word) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Word Detail</h1>
      <div className="bg-white p-4 rounded shadow">
        <p><strong>Kanji:</strong> {word.kanji}</p>
        <p><strong>Romaji:</strong> {word.romaji}</p>
        <p><strong>English:</strong> {word.english}</p>
        <p><strong>Correct Count:</strong> {word.correct_count}</p>
        <p><strong>Wrong Count:</strong> {word.wrong_count}</p>
        <p><strong>Groups:</strong></p>
        <ul>
          {word.groups.map((group) => (
            <li key={group.id}>{group.name}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

// --- Groups ---
function GroupList() {
    const [groups, setGroups] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const data = await fetchData(`/groups?page=${currentPage}`);
                setGroups(data.groups);
                setTotalPages(data.total_pages);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchGroups();
    }, [currentPage]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Groups</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {groups.map(group => (
                    <div key={group.id} className="bg-white p-4 rounded shadow">
                        <Link to={`/groups/${group.id}`} className="text-xl font-semibold text-blue-600 hover:underline">
                            {group.group_name}
                        </Link>
                        <p className="text-gray-500">Words: {group.word_count}</p>
                    </div>
                ))}
            </div>
            <div className="mt-4 flex justify-between">
                <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage <= 1}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage >= totalPages}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    );
}

function GroupDetail() {
    const { id } = useParams();
    const [group, setGroup] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchGroup = async () => {
            try {
                const data = await fetchData(`/groups/${id}`);
                setGroup(data);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchGroup();
    }, [id]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!group) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">{group.group_name}</h1>
            <p className="text-gray-500">Words: {group.word_count}</p>
            <div className="mt-4">
                <Link to={`/groups/${id}/words`} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                    View Words
                </Link>
                <Link to={`/groups/${id}/study_sessions`} className="ml-2 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
                    View Study Sessions
                </Link>
            </div>
        </div>
    );
}

function GroupWords() {
    const { id } = useParams();
    const [words, setWords] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchWords = async () => {
            try {
                const data = await fetchData(`/groups/${id}/words?page=${currentPage}`);
                setWords(data.words);
                setTotalPages(data.total_pages);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchWords();
    }, [id, currentPage]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Words in Group</h1>
            <table className="min-w-full bg-white border border-gray-300">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">Kanji</th>
                        <th className="py-2 px-4 border-b">Romaji</th>
                        <th className="py-2 px-4 border-b">English</th>
                        <th className="py-2 px-4 border-b">Correct</th>
                        <th className="py-2 px-4 border-b">Wrong</th>
                    </tr>
                </thead>
                <tbody>
                    {words.map(word => (
                        <tr key={word.id}>
                            <td className="py-2 px-4 border-b">{word.kanji}</td>
                            <td className="py-2 px-4 border-b">{word.romaji}</td>
                            <td className="py-2 px-4 border-b">{word.english}</td>
                            <td className="py-2 px-4 border-b">{word.correct_count}</td>
                            <td className="py-2 px-4 border-b">{word.wrong_count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="mt-4 flex justify-between">
                <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage <= 1}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage >= totalPages}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    );
}

function GroupStudySessions() {
    const { id } = useParams();
    const [sessions, setSessions] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSessions = async () => {
            try {
                const data = await fetchData(`/groups/${id}/study_sessions?page=${currentPage}`);
                setSessions(data.study_sessions);
                setTotalPages(data.total_pages);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchSessions();
    }, [id, currentPage]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Study Sessions for Group</h1>
            <table className="min-w-full bg-white border border-gray-300">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">Activity</th>
                        <th className="py-2 px-4 border-b">Start Time</th>
                        <th className="py-2 px-4 border-b">End Time</th>
                        <th className="py-2 px-4 border-b">Review Items</th>
                    </tr>
                </thead>
                <tbody>
                    {sessions.map(session => (
                        <tr key={session.id}>
                            <td className="py-2 px-4 border-b">{session.activity_name}</td>
                            <td className="py-2 px-4 border-b">{new Date(session.start_time).toLocaleString()}</td>
                            <td className="py-2 px-4 border-b">{new Date(session.end_time).toLocaleString()}</td>
                            <td className="py-2 px-4 border-b">{session.review_items_count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="mt-4 flex justify-between">
                <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage <= 1}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage >= totalPages}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    );
}

// --- Study Activities ---
function StudyActivityList() {
    const [activities, setActivities] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchActivities = async () => {
            try {
                const data = await fetchData('/api/study-activities');
                setActivities(data);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchActivities();
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Study Activities</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {activities.map(activity => (
                    <div key={activity.id} className="bg-white p-4 rounded shadow">
                        <Link to={`/study-activities/${activity.id}`} className="text-xl font-semibold text-blue-600 hover:underline">
                            {activity.title}
                        </Link>
                        <p className="text-gray-500">
                            <a href={activity.launch_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                                Launch
                            </a>
                        </p>
                        <img src={activity.preview_url} alt={activity.title} className="mt-2 w-full h-auto rounded" />
                    </div>
                ))}
            </div>
        </div>
    );
}

function StudyActivityDetail() {
    const { id } = useParams();
    const [activity, setActivity] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchActivity = async () => {
            try {
                const data = await fetchData(`/api/study-activities/${id}`);
                setActivity(data);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchActivity();
    }, [id]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!activity) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">{activity.title}</h1>
            <p>
                <a href={activity.launch_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                    Launch Activity
                </a>
            </p>
            <img src={activity.preview_url} alt={activity.title} className="mt-2 w-full h-auto rounded" />
            <div className="mt-4">
                <Link to={`/study-activities/${id}/sessions`} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
                    View Sessions
                </Link>
            </div>
        </div>
    );
}

function StudyActivitySessions() {
    const { id } = useParams();
    const [sessions, setSessions] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSessions = async () => {
            try {
                const data = await fetchData(`/api/study-activities/${id}/sessions?page=${currentPage}`);
                setSessions(data.items);
                setTotalPages(data.total_pages);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchSessions();
    }, [id, currentPage]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Sessions for Activity</h1>
            <table className="min-w-full bg-white border border-gray-300">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">Group</th>
                        <th className="py-2 px-4 border-b">Start Time</th>
                        <th className="py-2 px-4 border-b">End Time</th>
                        <th className="py-2 px-4 border-b">Review Items</th>
                    </tr>
                </thead>
                <tbody>
                    {sessions.map(session => (
                        <tr key={session.id}>
                            <td className="py-2 px-4 border-b">{session.group_name}</td>
                            <td className="py-2 px-4 border-b">{new Date(session.start_time).toLocaleString()}</td>
                            <td className="py-2 px-4 border-b">{new Date(session.end_time).toLocaleString()}</td>
                            <td className="py-2 px-4 border-b">{session.review_items_count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="mt-4 flex justify-between">
                <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage <= 1}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage >= totalPages}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    );
}

// --- Study Sessions ---
function StudySessionList() {
    const [sessions, setSessions] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSessions = async () => {
            try {
                const data = await fetchData(`/api/study-sessions?page=${currentPage}`);
                setSessions(data.items);
                setTotalPages(data.total_pages);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchSessions();
    }, [currentPage]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Study Sessions</h1>
            <table className="min-w-full bg-white border border-gray-300">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">Group</th>
                        <th className="py-2 px-4 border-b">Activity</th>
                        <th className="py-2 px-4 border-b">Start Time</th>
                        <th className="py-2 px-4 border-b">End Time</th>
                        <th className="py-2 px-4 border-b">Review Items</th>
                    </tr>
                </thead>
                <tbody>
                    {sessions.map(session => (
                        <tr key={session.id}>
                            <td className="py-2 px-4 border-b">
                                <Link to={`/groups/${session.group_id}`} className="text-blue-500 hover:underline">
                                    {session.group_name}
                                </Link>
                            </td>
                            <td className="py-2 px-4 border-b">
                                <Link to={`/study-activities/${session.activity_id}`} className="text-blue-500 hover:underline">
                                    {session.activity_name}
                                </Link>
                            </td>
                            <td className="py-2 px-4 border-b">{new Date(session.start_time).toLocaleString()}</td>
                            <td className="py-2 px-4 border-b">{new Date(session.end_time).toLocaleString()}</td>
                            <td className="py-2 px-4 border-b">{session.review_items_count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="mt-4 flex justify-between">
                <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage <= 1}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage >= totalPages}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    );
}

function StudySessionDetail() {
    const { id } = useParams();
    const [session, setSession] = useState(null);
    const [words, setWords] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchSession = async () => {
            try {
                const data = await fetchData(`/api/study-sessions/${id}?page=${currentPage}`);
                setSession(data.session);
                setWords(data.words);
                setTotalPages(data.total_pages);
            } catch (err) {
                setError(err.message);
            }
        };
        fetchSession();
    }, [id, currentPage]);

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!session) {
        return <div>Loading...</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Study Session Details</h1>
            <div className="bg-white p-4 rounded shadow mb-4">
                <p><strong>Group:</strong> {session.group_name}</p>
                <p><strong>Activity:</strong> {session.activity_name}</p>
                <p><strong>Start Time:</strong> {new Date(session.start_time).toLocaleString()}</p>
                <p><strong>End Time:</strong> {new Date(session.end_time).toLocaleString()}</p>
                <p><strong>Review Items:</strong> {session.review_items_count}</p>
            </div>

            <h2 className="text-2xl font-semibold mb-2">Words Reviewed</h2>
            <table className="min-w-full bg-white border border-gray-300">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border-b">Kanji</th>
                        <th className="py-2 px-4 border-b">Romaji</th>
                        <th className="py-2 px-4 border-b">English</th>
                        <th className="py-2 px-4 border-b">Correct</th>
                        <th className="py-2 px-4 border-b">Wrong</th>
                    </tr>
                </thead>
                <tbody>
                    {words.map(word => (
                        <tr key={word.id}>
                            <td className="py-2 px-4 border-b">{word.kanji}</td>
                            <td className="py-2 px-4 border-b">{word.romaji}</td>
                            <td className="py-2 px-4 border-b">{word.english}</td>
                            <td className="py-2 px-4 border-b">{word.correct_count}</td>
                            <td className="py-2 px-4 border-b">{word.wrong_count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="mt-4 flex justify-between">
                <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage <= 1}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Previous
                </button>
                <span>Page {currentPage} of {totalPages}</span>
                <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage >= totalPages}
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                >
                    Next
                </button>
            </div>
        </div>
    );
}

// --- Main App ---
function App() {
  return (
    <Router>
      <nav className="bg-gray-800 text-white p-4">
        <ul className="flex space-x-4">
          <li><Link to="/" className="hover:text-gray-300">Dashboard</Link></li>
          <li><Link to="/words" className="hover:text-gray-300">Words</Link></li>
          <li><Link to="/groups" className="hover:text-gray-300">Groups</Link></li>
          <li><Link to="/study-activities" className="hover:text-gray-300">Study Activities</Link></li>
          <li><Link to="/study-sessions" className="hover:text-gray-300">Study Sessions</Link></li>

        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />

        <Route path="/words" element={<WordList />} />
        <Route path="/words/:word_id" element={<WordDetail />} />

        <Route path="/groups" element={<GroupList />} />
        <Route path="/groups/:id" element={<GroupDetail />} />
        <Route path="/groups/:id/words" element={<GroupWords />} />
        <Route path="/groups/:id/study_sessions" element={<GroupStudySessions />} />

        <Route path="/study-activities" element={<StudyActivityList />} />
        <Route path="/study-activities/:id" element={<StudyActivityDetail />} />
        <Route path="/study-activities/:id/sessions" element={<StudyActivitySessions />} />

        <Route path="/study-sessions" element={<StudySessionList />} />
        <Route path="/study-sessions/:id" element={<StudySessionDetail />} />
      </Routes>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById('artifact_react'));