import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Settings, TrendingUp, Clock, Tv } from 'lucide-react';

const TVScheduleGA = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [generation, setGeneration] = useState(0);
  const [bestFitness, setBestFitness] = useState(0);
  const [schedule, setSchedule] = useState([]);
  const [fitnessHistory, setFitnessHistory] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  
  // GA Parameters
  const [params, setParams] = useState({
    generations: 100,
    populationSize: 50,
    crossoverRate: 0.8,
    mutationRate: 0.2,
    elitismSize: 2
  });

  // Sample programs and ratings
  const programs = ['News', 'Drama', 'Comedy', 'Sports', 'Reality', 'Documentary'];
  const timeSlots = Array.from({ length: 18 }, (_, i) => i + 6);
  
  // Generate random ratings for demo
  const generateRatings = () => {
    const ratings = {};
    programs.forEach(program => {
      ratings[program] = timeSlots.map(() => Math.random() * 10);
    });
    return ratings;
  };

  const [ratings] = useState(generateRatings());

  const calculateFitness = (sched) => {
    return sched.reduce((total, program, idx) => {
      return total + (ratings[program]?.[idx] || 0);
    }, 0);
  };

  const createRandomSchedule = () => {
    return timeSlots.map(() => programs[Math.floor(Math.random() * programs.length)]);
  };

  const crossover = (parent1, parent2) => {
    const point = Math.floor(Math.random() * (parent1.length - 2)) + 1;
    const child1 = [...parent1.slice(0, point), ...parent2.slice(point)];
    const child2 = [...parent2.slice(0, point), ...parent1.slice(point)];
    return [child1, child2];
  };

  const mutate = (sched) => {
    const newSched = [...sched];
    const point = Math.floor(Math.random() * newSched.length);
    newSched[point] = programs[Math.floor(Math.random() * programs.length)];
    return newSched;
  };

  const runGeneticAlgorithm = () => {
    let population = Array(params.populationSize).fill(null).map(() => createRandomSchedule());
    let currentGen = 0;
    let history = [];

    const interval = setInterval(() => {
      if (currentGen >= params.generations) {
        clearInterval(interval);
        setIsRunning(false);
        return;
      }

      // Evaluate and sort
      const evaluated = population.map(s => ({
        schedule: s,
        fitness: calculateFitness(s)
      })).sort((a, b) => b.fitness - a.fitness);

      const best = evaluated[0];
      setGeneration(currentGen);
      setBestFitness(best.fitness);
      setSchedule(best.schedule);
      history.push(best.fitness);
      setFitnessHistory([...history]);

      // Create new population
      const newPop = evaluated.slice(0, params.elitismSize).map(e => e.schedule);

      while (newPop.length < params.populationSize) {
        const parent1 = evaluated[Math.floor(Math.random() * params.populationSize / 2)].schedule;
        const parent2 = evaluated[Math.floor(Math.random() * params.populationSize / 2)].schedule;

        let [child1, child2] = Math.random() < params.crossoverRate 
          ? crossover(parent1, parent2)
          : [[...parent1], [...parent2]];

        if (Math.random() < params.mutationRate) child1 = mutate(child1);
        if (Math.random() < params.mutationRate) child2 = mutate(child2);

        newPop.push(child1, child2);
      }

      population = newPop.slice(0, params.populationSize);
      currentGen++;
    }, 50);
  };

  const handleStart = () => {
    setIsRunning(true);
    runGeneticAlgorithm();
  };

  const handleReset = () => {
    setIsRunning(false);
    setGeneration(0);
    setBestFitness(0);
    setSchedule([]);
    setFitnessHistory([]);
  };

  const getColorForProgram = (program) => {
    const colors = {
      'News': 'bg-blue-500',
      'Drama': 'bg-purple-500',
      'Comedy': 'bg-yellow-500',
      'Sports': 'bg-green-500',
      'Reality': 'bg-pink-500',
      'Documentary': 'bg-orange-500'
    };
    return colors[program] || 'bg-gray-500';
  };

  const maxFitness = Math.max(...fitnessHistory, 1);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Tv className="w-10 h-10 text-purple-400" />
            <h1 className="text-4xl font-bold text-white">TV Scheduling Optimizer</h1>
          </div>
          <p className="text-purple-300">Genetic Algorithm-Based Program Scheduling</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center gap-3">
              <TrendingUp className="w-8 h-8 text-green-400" />
              <div>
                <p className="text-purple-300 text-sm">Generation</p>
                <p className="text-white text-2xl font-bold">{generation}</p>
              </div>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center gap-3">
              <TrendingUp className="w-8 h-8 text-blue-400" />
              <div>
                <p className="text-purple-300 text-sm">Best Fitness</p>
                <p className="text-white text-2xl font-bold">{bestFitness.toFixed(2)}</p>
              </div>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <div className="flex items-center gap-3">
              <Clock className="w-8 h-8 text-yellow-400" />
              <div>
                <p className="text-purple-300 text-sm">Time Slots</p>
                <p className="text-white text-2xl font-bold">{timeSlots.length}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-6">
          <div className="flex flex-wrap items-center gap-4">
            <button
              onClick={handleStart}
              disabled={isRunning}
              className="flex items-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 disabled:bg-gray-500 text-white rounded-lg font-semibold transition-colors"
            >
              <Play className="w-5 h-5" />
              Start Algorithm
            </button>

            <button
              onClick={handleReset}
              className="flex items-center gap-2 px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg font-semibold transition-colors"
            >
              <RotateCcw className="w-5 h-5" />
              Reset
            </button>

            <button
              onClick={() => setShowSettings(!showSettings)}
              className="flex items-center gap-2 px-6 py-3 bg-purple-500 hover:bg-purple-600 text-white rounded-lg font-semibold transition-colors"
            >
              <Settings className="w-5 h-5" />
              Parameters
            </button>
          </div>

          {showSettings && (
            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(params).map(([key, value]) => (
                <div key={key}>
                  <label className="block text-purple-300 text-sm mb-2 capitalize">
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </label>
                  <input
                    type="number"
                    value={value}
                    onChange={(e) => setParams({ ...params, [key]: parseFloat(e.target.value) })}
                    className="w-full px-4 py-2 bg-white/20 border border-white/30 rounded-lg text-white"
                    disabled={isRunning}
                  />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Fitness Chart */}
        {fitnessHistory.length > 0 && (
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-6">
            <h3 className="text-xl font-bold text-white mb-4">Fitness Progress</h3>
            <div className="h-48 flex items-end gap-1">
              {fitnessHistory.map((fitness, idx) => (
                <div
                  key={idx}
                  className="flex-1 bg-gradient-to-t from-purple-500 to-blue-500 rounded-t transition-all"
                  style={{ height: `${(fitness / maxFitness) * 100}%` }}
                  title={`Gen ${idx}: ${fitness.toFixed(2)}`}
                />
              ))}
            </div>
          </div>
        )}

        {/* Schedule Display */}
        {schedule.length > 0 && (
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <h3 className="text-xl font-bold text-white mb-4">Optimal Schedule</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {schedule.map((program, idx) => (
                <div
                  key={idx}
                  className="bg-white/20 rounded-lg p-4 border border-white/30 hover:bg-white/30 transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-purple-300 text-sm font-semibold">
                        {String(timeSlots[idx]).padStart(2, '0')}:00 - {String(timeSlots[idx] + 1).padStart(2, '0')}:00
                      </p>
                      <p className="text-white text-lg font-bold">{program}</p>
                    </div>
                    <div className={`w-12 h-12 ${getColorForProgram(program)} rounded-full flex items-center justify-center text-white font-bold`}>
                      {ratings[program]?.[idx]?.toFixed(1) || '0'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Legend */}
        <div className="mt-6 bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
          <h3 className="text-lg font-bold text-white mb-3">Program Types</h3>
          <div className="flex flex-wrap gap-4">
            {programs.map(program => (
              <div key={program} className="flex items-center gap-2">
                <div className={`w-4 h-4 ${getColorForProgram(program)} rounded`} />
                <span className="text-purple-300">{program}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TVScheduleGA;
