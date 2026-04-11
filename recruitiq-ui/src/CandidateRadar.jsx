import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer } from 'recharts';

export default function CandidateRadar({ score }) {
  // Mock data for the radar - we can derive this from the score and random jitters for demo
  const data = [
    { subject: 'Skill Match', A: Math.min(100, score + 5), fullMark: 100 },
    { subject: 'Experience', A: Math.max(70, score - 10), fullMark: 100 },
    { subject: 'Semantic Fit', A: score, fullMark: 100 },
    { subject: 'NLP Depth', A: Math.max(60, score - 15), fullMark: 100 },
    { subject: 'Deployment', A: Math.max(50, score - 20), fullMark: 100 },
  ];

  return (
    <div className="w-24 h-24 opacity-60 group-hover:opacity-100 transition-opacity">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
          <PolarGrid stroke="#ffffff20" />
          <PolarAngleAxis dataKey="subject" tick={false} />
          <Radar
            name="Candidate"
            dataKey="A"
            stroke="#7b61ff"
            fill="#7b61ff"
            fillOpacity={0.5}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
