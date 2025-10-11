import React from 'react';
import { motion } from 'framer-motion';
import { BarChart3, CheckCircle2, Clock, AlertCircle, TrendingUp } from 'lucide-react';

export default function TaskStats({ stats }) {
  const statCards = [
    {
      title: 'Total Tasks',
      value: stats.total,
      icon: BarChart3,
      gradient: 'from-amber-400 to-yellow-500',
      bgGradient: 'from-amber-500/20 to-yellow-500/20',
      borderColor: 'border-amber-400/30',
    },
    {
      title: 'Completed',
      value: stats.completed,
      icon: CheckCircle2,
      gradient: 'from-emerald-400 to-green-500',
      bgGradient: 'from-emerald-500/20 to-green-500/20',
      borderColor: 'border-emerald-400/30',
    },
    {
      title: 'Pending',
      value: stats.pending,
      icon: Clock,
      gradient: 'from-blue-400 to-cyan-500',
      bgGradient: 'from-blue-500/20 to-cyan-500/20',
      borderColor: 'border-blue-400/30',
    },
    {
      title: 'Overdue',
      value: stats.overdue,
      icon: AlertCircle,
      gradient: 'from-red-400 to-pink-500',
      bgGradient: 'from-red-500/20 to-pink-500/20',
      borderColor: 'border-red-400/30',
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.15 }}
      className="mb-8"
    >
      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            whileHover={{ scale: 1.05 }}
            className={`p-4 glass rounded-xl border ${stat.borderColor} bg-gradient-to-br ${stat.bgGradient} hover:shadow-lg transition-all duration-200`}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-amber-100/90 text-sm font-medium mb-1">
                  {stat.title}
                </p>
                <p className="text-2xl font-bold text-amber-100">
                  {stat.value}
                </p>
              </div>
              <div className={`p-2 rounded-lg bg-gradient-to-r ${stat.gradient}`}>
                <stat.icon className="w-5 h-5 text-slate-900" />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Progress Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        className="p-6 glass rounded-2xl border border-amber-400/20 bg-slate-800/40"
      >
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-to-r from-amber-400 to-yellow-500">
              <TrendingUp className="w-5 h-5 text-slate-900" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-amber-100">
                Progress Overview
              </h3>
              <p className="text-amber-200/70 text-sm">
                Your productivity metrics
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-amber-100">
              {stats.completion_rate}%
            </p>
            <p className="text-amber-200/70 text-sm">
              Completion Rate
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="relative h-3 bg-slate-700/40 rounded-full overflow-hidden mb-4">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${stats.completion_rate}%` }}
            transition={{ duration: 1, delay: 0.5 }}
            className="h-full bg-gradient-to-r from-amber-400 to-yellow-500 rounded-full"
          />
        </div>

        {/* Additional Stats */}
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="text-center p-3 bg-slate-700/30 rounded-lg border border-amber-400/20">
            <p className="text-amber-100 font-semibold">
              {stats.today_completed}
            </p>
            <p className="text-amber-200/70">
              Completed Today
            </p>
          </div>
          <div className="text-center p-3 bg-slate-700/30 rounded-lg border border-amber-400/20">
            <p className="text-amber-100 font-semibold">
              {stats.this_week_completed}
            </p>
            <p className="text-amber-200/70">
              This Week
            </p>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}
