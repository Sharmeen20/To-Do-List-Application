import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { X, Star, Calendar, Tag } from 'lucide-react';
import toast from 'react-hot-toast';

// API Service without authentication
const apiService = {
  async getCategories() {
    const response = await fetch('http://localhost:8000/api/categories/', {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Failed to fetch categories');
    return response.json();
  },
  
  async createTask(taskData) {
    const response = await fetch('http://localhost:8000/api/tasks/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });
    if (!response.ok) throw new Error('Failed to create task');
    return response.json();
  },
  
  async updateTask(id, taskData) {
    const response = await fetch(`http://localhost:8000/api/tasks/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(taskData),
    });
    if (!response.ok) throw new Error('Failed to update task');
    return response.json();
  }
};

export default function TaskModal({ isOpen, onClose, task, onSave }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'medium',
    due_date: '',
    category: null,
  });
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchCategories();
      if (task) {
        setFormData({
          title: task.title || '',
          description: task.description || '',
          priority: task.priority || 'medium',
          due_date: task.due_date ? task.due_date.split('T')[0] : '',
          category: task.category || null,
        });
      } else {
        setFormData({
          title: '',
          description: '',
          priority: 'medium',
          due_date: '',
          category: null,
        });
      }
    }
  }, [isOpen, task]);

  const fetchCategories = async () => {
    try {
      const data = await apiService.getCategories();
      setCategories(data.results || data);
    } catch (error) {
      toast.error('Failed to load categories');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const taskData = {
        ...formData,
        due_date: formData.due_date ? new Date(formData.due_date).toISOString() : null,
      };
      
      if (task) {
        const updatedTask = await apiService.updateTask(task.id, taskData);
        onSave(updatedTask);
        toast.success('Task updated successfully');
      } else {
        const newTask = await apiService.createTask(taskData);
        onSave(newTask);
        toast.success('Task created successfully');
      }
      
      onClose();
    } catch (error) {
      toast.error('Failed to save task');
    }
    setLoading(false);
  };

  if (!isOpen) return null;

  const priorityColors = {
    low: 'bg-emerald-400/20 text-emerald-300 border-emerald-400/30',
    medium: 'bg-amber-400/20 text-amber-300 border-amber-400/30',
    high: 'bg-red-400/20 text-red-300 border-red-400/30',
  };

  return (
    <div className="fixed inset-0 bg-slate-900/80 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.9, y: 20 }}
        className="glass bg-slate-800/90 backdrop-blur-xl border border-amber-500/20 rounded-2xl shadow-2xl shadow-amber-500/10 max-w-md w-full p-8 relative"
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-amber-300/60 hover:text-amber-300 hover:bg-amber-500/10 rounded-full transition-all duration-200"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-r from-amber-400 to-yellow-500 rounded-xl shadow-lg shadow-amber-500/25">
            <Star className="w-5 h-5 text-slate-900" />
          </div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-amber-200 via-yellow-300 to-amber-400 bg-clip-text text-transparent">
            {task ? 'Edit Task' : 'Create New Task'}
          </h2>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Task Title */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-amber-200/90">
              Task Title
            </label>
            <input
              type="text"
              placeholder="Enter task title..."
              value={formData.title}
              onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
              className="w-full px-4 py-3 bg-slate-700/50 border border-amber-400/30 rounded-xl text-amber-100 placeholder-amber-300/60 focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/60 outline-none transition-all duration-200"
              required
            />
          </div>
          
          {/* Description */}
          <div className="space-y-2">
            <label className="block text-sm font-medium text-amber-200/90">
              Description
            </label>
            <textarea
              placeholder="Add a description (optional)..."
              value={formData.description}
              onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
              className="w-full px-4 py-3 bg-slate-700/50 border border-amber-400/30 rounded-xl text-amber-100 placeholder-amber-300/60 focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/60 outline-none transition-all duration-200 resize-none"
              rows={3}
            />
          </div>
          
          {/* Priority and Due Date */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm font-medium text-amber-200/90">
                <Star className="w-4 h-4" />
                Priority
              </label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData(prev => ({ ...prev, priority: e.target.value }))}
                className="w-full px-4 py-3 bg-slate-700/50 border border-amber-400/30 rounded-xl text-amber-100 focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/60 outline-none transition-all duration-200"
              >
                <option value="low" className="bg-slate-800">Low Priority</option>
                <option value="medium" className="bg-slate-800">Medium Priority</option>
                <option value="high" className="bg-slate-800">High Priority</option>
              </select>
            </div>
            
            <div className="space-y-2">
              <label className="flex items-center gap-2 text-sm font-medium text-amber-200/90">
                <Calendar className="w-4 h-4" />
                Due Date
              </label>
              <input
                type="date"
                value={formData.due_date}
                onChange={(e) => setFormData(prev => ({ ...prev, due_date: e.target.value }))}
                className="w-full px-4 py-3 bg-slate-700/50 border border-amber-400/30 rounded-xl text-amber-100 focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/60 outline-none transition-all duration-200"
              />
            </div>
          </div>
          
          {/* Category */}
          <div className="space-y-2">
            <label className="flex items-center gap-2 text-sm font-medium text-amber-200/90">
              <Tag className="w-4 h-4" />
              Category
            </label>
            <select
              value={formData.category || ''}
              onChange={(e) => setFormData(prev => ({ 
                ...prev, 
                category: e.target.value ? parseInt(e.target.value) : null 
              }))}
              className="w-full px-4 py-3 bg-slate-700/50 border border-amber-400/30 rounded-xl text-amber-100 focus:ring-2 focus:ring-amber-400/50 focus:border-amber-400/60 outline-none transition-all duration-200"
            >
              <option value="" className="bg-slate-800">No Category</option>
              {categories.map(category => (
                <option key={category.id} value={category.id} className="bg-slate-800">
                  {category.name}
                </option>
              ))}
            </select>
          </div>
          
          {/* Action Buttons */}
          <div className="flex gap-4 pt-6">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 px-4 bg-slate-700/50 border border-amber-400/30 text-amber-200 rounded-xl hover:bg-slate-600/50 hover:border-amber-400/50 transition-all duration-200 font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 py-3 px-4 bg-gradient-to-r from-amber-500 to-yellow-500 text-slate-900 rounded-xl hover:from-amber-400 hover:to-yellow-400 disabled:from-slate-600 disabled:to-slate-600 disabled:text-slate-400 disabled:cursor-not-allowed transition-all duration-200 font-medium shadow-lg shadow-amber-500/25"
            >
              {loading ? 'Saving...' : task ? 'Update Task' : 'Create Task'}
            </button>
          </div>
        </form>
      </motion.div>
    </div>
  );
}
