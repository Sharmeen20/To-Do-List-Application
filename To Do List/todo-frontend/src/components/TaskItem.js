import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, Square, Trash2, Edit3, Calendar, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

// API Service
const apiService = {
  async deleteTask(id) {
    const response = await fetch(`http://localhost:8000/api/tasks/${id}/`, { 
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (!response.ok) throw new Error('Failed to delete task');
    // Handle 204 No Content response
    return null;
  }
};

export default function TaskItem({ task, onUpdate, onDelete, onEdit }) {
  const handleToggle = async () => {
    try {
      await onUpdate(task.id, { is_done: !task.is_done });
      toast.success(task.is_done ? 'Task marked as pending' : 'Task completed!');
    } catch (error) {
      toast.error('Failed to update task');
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await apiService.deleteTask(task.id);
        onDelete(task.id);
        toast.success('Task deleted');
      } catch (error) {
        toast.error('Failed to delete task');
      }
    }
  };

  const formatDueDate = (dueDate) => {
    if (!dueDate) return null;
    const date = new Date(dueDate);
    const now = new Date();
    const diffTime = date - now;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays < 0) {
      return { text: `${Math.abs(diffDays)} days overdue`, color: 'text-red-400', urgent: true };
    } else if (diffDays === 0) {
      return { text: 'Due today', color: 'text-amber-400', urgent: true };
    } else if (diffDays === 1) {
      return { text: 'Due tomorrow', color: 'text-amber-300', urgent: false };
    } else {
      return { text: `Due in ${diffDays} days`, color: 'text-amber-200/70', urgent: false };
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-500/20 text-red-300 border-red-400/30';
      case 'medium': return 'bg-amber-500/20 text-amber-300 border-amber-400/30';
      case 'low': return 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30';
      default: return 'bg-slate-500/20 text-slate-300 border-slate-400/30';
    }
  };

  const dueDateInfo = formatDueDate(task.due_date);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ scale: 1.02 }}
      className={`p-4 glass rounded-xl border transition-all duration-200 ${
        task.is_done 
          ? 'border-emerald-400/20 bg-emerald-900/10' 
          : dueDateInfo?.urgent 
            ? 'border-red-400/30 bg-red-900/10' 
            : 'border-amber-400/20 bg-slate-800/40'
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Toggle Button */}
        <button
          onClick={handleToggle}
          className={`mt-1 p-1 rounded-lg transition-all duration-200 ${
            task.is_done
              ? 'text-emerald-400 hover:bg-emerald-500/10'
              : 'text-amber-300 hover:bg-amber-500/10'
          }`}
        >
          {task.is_done ? (
            <CheckCircle2 className="w-5 h-5" />
          ) : (
            <Square className="w-5 h-5" />
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <h3 className={`font-medium transition-all duration-200 ${
                task.is_done 
                  ? 'text-amber-200/60 line-through' 
                  : 'text-amber-100'
              }`}>
                {task.title}
              </h3>
              
              {task.description && (
                <p className={`text-sm mt-1 transition-all duration-200 ${
                  task.is_done 
                    ? 'text-amber-200/40 line-through' 
                    : 'text-amber-200/70'
                }`}>
                  {task.description}
                </p>
              )}
              
              {/* Tags and Due Date */}
              <div className="flex flex-wrap items-center gap-2 mt-3">
                {/* Priority Badge */}
                <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getPriorityColor(task.priority)}`}>
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>
                
                {/* Category Badge */}
                {task.category_name && (
                  <span 
                    className="px-2 py-1 text-xs font-medium rounded-full border border-amber-400/30"
                    style={{ 
                      backgroundColor: task.category_color ? `${task.category_color}20` : 'rgba(251, 191, 36, 0.1)',
                      color: task.category_color || '#fbbf24'
                    }}
                  >
                    {task.category_name}
                  </span>
                )}
                
                {/* Due Date */}
                {dueDateInfo && (
                  <div className={`flex items-center gap-1 text-xs ${dueDateInfo.color}`}>
                    {dueDateInfo.urgent ? (
                      <AlertCircle className="w-3 h-3" />
                    ) : (
                      <Calendar className="w-3 h-3" />
                    )}
                    <span>{dueDateInfo.text}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-1">
              <button
                onClick={() => onEdit(task)}
                className="p-2 text-amber-300/60 hover:text-amber-300 hover:bg-amber-500/10 rounded-lg transition-all duration-200"
              >
                <Edit3 className="w-4 h-4" />
              </button>
              <button
                onClick={handleDelete}
                className="p-2 text-red-300/60 hover:text-red-300 hover:bg-red-500/10 rounded-lg transition-all duration-200"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
