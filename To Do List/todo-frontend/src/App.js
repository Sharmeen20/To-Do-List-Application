import React, { useState, useEffect } from 'react';
import { 
  Plus, CheckCircle2, Square, Trash2, Edit3, Calendar, 
  Search, Clock, AlertCircle, BarChart3
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import toast, { Toaster } from 'react-hot-toast';

// Import components
import TaskModal from './components/TaskModal';
import TaskItem from './components/TaskItem';
import TaskStats from './components/TaskStats';

const API_BASE = 'http://localhost:8000/api';

// API Service
class ApiService {
  constructor() {
    this.baseUrl = API_BASE;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
        ...options,
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(errorData || `HTTP error! status: ${response.status}`);
      }

      // Handle responses with no content (like DELETE requests)
      if (response.status === 204 || response.headers.get('content-length') === '0') {
        return null;
      }

      return response.json();
    } catch (error) {
      console.error('API Request failed:', error);
      throw error;
    }
  }

  // Task methods
  async getTasks(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/tasks/${queryString ? '?' + queryString : ''}`);
  }

  async createTask(taskData) {
    return this.request('/tasks/', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async updateTask(id, taskData) {
    return this.request(`/tasks/${id}/`, {
      method: 'PATCH',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(id) {
    return this.request(`/tasks/${id}/`, { method: 'DELETE' });
  }

  async getTaskStats() {
    return this.request('/tasks/stats/');
  }

  // Category methods
  async getCategories() {
    return this.request('/categories/');
  }

  async createCategory(categoryData) {
    return this.request('/categories/', {
      method: 'POST',
      body: JSON.stringify(categoryData),
    });
  }
}

const apiService = new ApiService();

function App() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [hasAttemptedLoad, setHasAttemptedLoad] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  useEffect(() => {
    fetchTasks();
    fetchStats();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      setHasAttemptedLoad(true);
      const response = await apiService.getTasks();
      setTasks(response.results || response);
    } catch (err) {
      setError('Failed to load tasks. Please try again.');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const statsData = await apiService.getTaskStats();
      setStats(statsData);
    } catch (err) {
      // Set default stats if fetch fails
      setStats({
        total: 0,
        completed: 0,
        pending: 0,
        overdue: 0,
        completion_rate: 0,
        today_completed: 0,
        this_week_completed: 0
      });
      console.error('Error fetching stats:', err);
    }
  };

  const handleTaskUpdate = async (taskId, updates) => {
    try {
      const updatedTask = await apiService.updateTask(taskId, updates);
      setTasks(prev => prev.map(task => 
        task.id === taskId ? updatedTask : task
      ));
      fetchStats();
      toast.success('Task updated');
    } catch (error) {
      toast.error('Failed to update task');
    }
  };

  const handleTaskCreate = (newTask) => {
    setTasks(prev => [newTask, ...prev]);
    fetchStats();
  };

  const handleTaskDelete = (taskId) => {
    setTasks(prev => prev.filter(task => task.id !== taskId));
    fetchStats();
  };

  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         task.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesStatus = filterStatus === 'all' || 
                         (filterStatus === 'pending' && !task.is_done) ||
                         (filterStatus === 'completed' && task.is_done);
    
    return matchesSearch && matchesStatus;
  });

  const pendingTasks = filteredTasks.filter(task => !task.is_done);
  const completedTasks = filteredTasks.filter(task => task.is_done);

  if (loading && tasks.length === 0) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-2xl font-semibold text-amber-200 animate-pulse">
          Loading your tasks...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-slate-900 relative">
      {/* Deep Navy & Gold Background */}
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `
            radial-gradient(circle at 50% 50%, 
              rgba(251, 191, 36, 0.15) 0%, 
              rgba(251, 191, 36, 0.08) 25%, 
              rgba(251, 191, 36, 0.03) 35%, 
              transparent 50%
            )
          `,
          backgroundSize: "100% 100%",
        }}
      />
      
      {/* Subtle animated elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-amber-400/10 rounded-full filter blur-3xl animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-yellow-400/10 rounded-full filter blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute top-1/3 left-1/3 w-80 h-80 bg-amber-300/5 rounded-full filter blur-3xl animate-blob animation-delay-4000"></div>
      </div>
      
      <div className="relative z-10 container mx-auto px-6 py-12 md:px-8 lg:px-12">
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="flex items-center justify-between mb-8"
        >
          <div className="flex items-center gap-4">
            <div className="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-amber-400 to-yellow-500 rounded-xl shadow-lg shadow-amber-500/25">
              <CheckCircle2 className="w-6 h-6 text-slate-900" />
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-amber-200 via-yellow-300 to-amber-400 bg-clip-text text-transparent">
                TodoMaster
              </h1>
              <p className="text-sm text-amber-200/80 font-light">
                Transform your productivity with elegance ✨
              </p>
            </div>
          </div>
          
          {/* Quick Stats in Header */}
          <div className="hidden md:flex items-center gap-4">
            <div className="text-right">
              <div className="text-sm text-amber-200/60">Today's Progress</div>
              <div className="text-amber-100 font-semibold">
                {stats ? `${stats.completed}/${stats.total} tasks` : '0/0 tasks'}
              </div>
            </div>
            <div className="w-12 h-12 rounded-full bg-gradient-to-r from-amber-500/20 to-yellow-500/20 border border-amber-400/30 flex items-center justify-center">
              <span className="text-amber-300 font-bold">
                {stats && stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0}%
              </span>
            </div>
          </div>
        </motion.div>

        {/* Error Message */}
        <AnimatePresence>
          {error && hasAttemptedLoad && !loading && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-6 p-4 glass rounded-xl border border-red-400/30 bg-red-900/20"
            >
              <div className="flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-400" />
                <span className="text-red-200">{error}</span>
                <button
                  onClick={fetchTasks}
                  className="ml-auto text-red-300 hover:text-amber-200 underline transition-colors"
                >
                  Retry
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Controls */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="mb-8 p-6 glass bg-slate-800/40 rounded-2xl border border-amber-500/20 shadow-xl"
        >
          <div className="flex flex-col sm:flex-row gap-4 items-center">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-amber-300 w-5 h-5" />
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-slate-700/50 border border-amber-400/30 rounded-xl text-amber-100 placeholder-amber-300/60 focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/60 outline-none transition-all"
              />
            </div>
            
            <div className="flex gap-3">
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-4 py-3 bg-slate-700/50 border border-amber-400/30 rounded-xl text-amber-100 focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/60 outline-none"
              >
                <option value="all">All Tasks</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
              </select>
              
              <button
                onClick={() => setIsModalOpen(true)}
                className="px-6 py-3 bg-gradient-to-r from-amber-500 to-yellow-500 text-slate-900 rounded-xl hover:from-amber-400 hover:to-yellow-400 transition-all shadow-lg shadow-amber-500/25 font-medium flex items-center gap-2"
              >
                <Plus className="w-5 h-5" />
                Add Task
              </button>
            </div>
          </div>
        </motion.div>

        {/* Task Stats */}
        {stats && <TaskStats stats={stats} />}

        {/* Task Lists */}
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Pending Tasks */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="space-y-4"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-amber-500 to-yellow-500 flex items-center justify-center">
                <Clock className="w-4 h-4 text-slate-900" />
              </div>
              <h2 className="text-xl font-semibold text-amber-100">
                Pending Tasks
              </h2>
              <div className="px-3 py-1 bg-amber-500/20 text-amber-300 rounded-full text-sm font-medium border border-amber-400/30">
                {pendingTasks.length}
              </div>
            </div>
            
            <div className="space-y-3">
              <AnimatePresence>
                {pendingTasks.map(task => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onUpdate={handleTaskUpdate}
                    onDelete={handleTaskDelete}
                    onEdit={(task) => {
                      setEditingTask(task);
                      setIsModalOpen(true);
                    }}
                  />
                ))}
              </AnimatePresence>
              
              {pendingTasks.length === 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-12 glass rounded-2xl border border-amber-500/20"
                >
                  <Plus className="w-16 h-16 text-amber-400/40 mx-auto mb-4" />
                  <p className="text-amber-200/60 mb-4">No pending tasks</p>
                  <button
                    onClick={() => setIsModalOpen(true)}
                    className="px-4 py-2 bg-gradient-to-r from-amber-500 to-yellow-500 text-slate-900 rounded-lg hover:from-amber-400 hover:to-yellow-400 transition-all font-medium"
                  >
                    Create your first task
                  </button>
                </motion.div>
              )}
            </div>
          </motion.div>

          {/* Completed Tasks */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="space-y-4"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-500 to-green-500 flex items-center justify-center">
                <CheckCircle2 className="w-4 h-4 text-slate-900" />
              </div>
              <h2 className="text-xl font-semibold text-amber-100">
                Completed Tasks
              </h2>
              <div className="px-3 py-1 bg-emerald-500/20 text-emerald-300 rounded-full text-sm font-medium border border-emerald-400/30">
                {completedTasks.length}
              </div>
            </div>
            
            <div className="space-y-3">
              <AnimatePresence>
                {completedTasks.map(task => (
                  <TaskItem
                    key={task.id}
                    task={task}
                    onUpdate={handleTaskUpdate}
                    onDelete={handleTaskDelete}
                    onEdit={(task) => {
                      setEditingTask(task);
                      setIsModalOpen(true);
                    }}
                  />
                ))}
              </AnimatePresence>
              
              {completedTasks.length === 0 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-center py-12 glass rounded-2xl border border-amber-500/20"
                >
                  <CheckCircle2 className="w-16 h-16 text-amber-400/40 mx-auto mb-4" />
                  <p className="text-amber-200/60">No completed tasks yet</p>
                </motion.div>
              )}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Task Modal */}
      <TaskModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingTask(null);
        }}
        task={editingTask}
        onSave={(task) => {
          if (editingTask) {
            setTasks(prev => prev.map(t => t.id === task.id ? task : t));
          } else {
            handleTaskCreate(task);
          }
          fetchStats();
        }}
      />

      {/* Toast Container */}
      <Toaster 
        position="top-right"
        toastOptions={{
          style: {
            background: 'rgba(30, 41, 59, 0.9)',
            color: '#f1f5f9',
            border: '1px solid rgba(251, 191, 36, 0.3)',
          },
        }}
      />
    </div>
  );
}

export default App;
