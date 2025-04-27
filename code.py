import { useState, useEffect, useMemo } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, ReferenceLine } from "recharts";

export default function BlackScholesCalculator() {
  const [S, setS] = useState(100);
  const [K, setK] = useState(105);
  const [T, setT] = useState(0.5);
  const [r, setR] = useState(0.05);
  const [sigma, setSigma] = useState(0.2);
  const [price, setPrice] = useState(null);
  const [isCall, setIsCall] = useState(true);
  const [simulating, setSimulating] = useState(false);

  const scenarios = [
    {
      name: "Compra de Call",
      S: 100,
      K: 105,
      T: 0.5,
      r: 0.05,
      sigma: 0.2,
      isCall: true,
    },
    {
      name: "Protección con Put",
      S: 1500,
      K: 1400,
      T: 1,
      r: 0.03,
      sigma: 0.25,
      isCall: false,
    },
    {
      name: "Impacto de Volatilidad",
      S: 200,
      K: 200,
      T: 0.5,
      r: 0.05,
      sigma: 0.5,
      isCall: true,
    },
  ];

  useEffect(() => {
    if (!simulating) return;
    const interval = setInterval(() => {
      setS((prev) => (prev >= 150 ? 50 : prev + 1));
    }, 200);
    return () => clearInterval(interval);
  }, [simulating]);

  const N = (x) => 0.5 * (1 + erf(x / Math.sqrt(2)));
  const erf = (x) => {
    const sign = x >= 0 ? 1 : -1;
    x = Math.abs(x);
    const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741;
    const a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
    const t = 1 / (1 + p * x);
    const y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return sign * y;
  };

  const calculateOptionPrice = (s) => {
    const d1 = (Math.log(s / K) + (r + sigma ** 2 / 2) * T) / (sigma * Math.sqrt(T));
    const d2 = d1 - sigma * Math.sqrt(T);
    const call = s * N(d1) - K * Math.exp(-r * T) * N(d2);
    const put = K * Math.exp(-r * T) * N(-d2) - s * N(-d1);
    return isCall ? call : put;
  };

  useEffect(() => {
    setPrice(calculateOptionPrice(S).toFixed(2));
  }, [S, K, T, r, sigma, isCall]);

  const chartData = useMemo(() => {
    return Array.from({ length: 50 }, (_, i) => {
      const s = 50 + i * 2;
      const value = calculateOptionPrice(s);
      return { S: s, Value: parseFloat(value.toFixed(2)) };
    });
  }, [K, T, r, sigma, isCall]);

  const InputLabel = ({ label, description }) => (
    <div className="flex flex-col text-sm text-white">
      <span className="font-semibold">{label}</span>
      <span className="text-zinc-400 text-xs leading-snug">{description}</span>
    </div>
  );

  const loadScenario = (scenario) => {
    setS(scenario.S);
    setK(scenario.K);
    setT(scenario.T);
    setR(scenario.r);
    setSigma(scenario.sigma);
    setIsCall(scenario.isCall);
  };

  return (
    <div className="p-6 bg-zinc-900 text-white rounded-2xl shadow-xl max-w-4xl mx-auto grid gap-6">
      <Card className="bg-zinc-800 border-zinc-700">
        <CardContent className="grid gap-4 p-6">
          <h1 className="text-2xl font-bold">Calculadora Black-Scholes ({isCall ? "Call" : "Put"})</h1>
          <div className="flex items-center gap-2">
            <span className="text-sm text-zinc-300">Call</span>
            <Switch checked={!isCall} onCheckedChange={() => setIsCall(!isCall)} />
            <span className="text-sm text-zinc-300">Put</span>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <div>
              <InputLabel label="Precio actual (S)" description="Valor del activo hoy (por ej. acción)" />
              <Input className="bg-zinc-700 text-white mt-1" type="number" value={S} onChange={(e) => setS(+e.target.value)} />
            </div>
            <div>
              <InputLabel label="Precio de ejercicio (K)" description="Precio al cual se puede ejercer la opción" />
              <Input className="bg-zinc-700 text-white mt-1" type="number" value={K} onChange={(e) => setK(+e.target.value)} />
            </div>
            <div>
              <InputLabel label="Tiempo (T)" description="Tiempo hasta el vencimiento (en años)" />
              <Input className="bg-zinc-700 text-white mt-1" type="number" step="0.01" value={T} onChange={(e) => setT(+e.target.value)} />
            </div>
            <div>
              <InputLabel label="Tasa libre de riesgo (r)" description="Tasa de interés anual (por ejemplo, bono del Tesoro)" />
              <Input className="bg-zinc-700 text-white mt-1" type="number" step="0.01" value={r} onChange={(e) => setR(+e.target.value)} />
            </div>
            <div>
              <InputLabel label="Volatilidad (σ)" description="Medida de incertidumbre o variabilidad del activo" />
              <Input className="bg-zinc-700 text-white mt-1" type="number" step="0.01" value={sigma} onChange={(e) => setSigma(+e.target.value)} />
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button onClick={() => setPrice(calculateOptionPrice(S).toFixed(2))} className="bg-indigo-600 hover:bg-indigo-500">Calcular precio del {isCall ? "Call" : "Put"}</Button>
            <Button onClick={() => setSimulating(!simulating)} className="bg-blue-700 hover:bg-blue-600">
              {simulating ? "Detener Simulación" : "Iniciar Simulación"}
            </Button>
            {scenarios.map((scenario, index) => (
              <Button key={index} onClick={() => loadScenario(scenario)} className="bg-green-700 hover:bg-green-600">
                {scenario.name}
              </Button>
            ))}
          </div>
          {price !== null && <p className="text-lg font-semibold text-green-400">Precio del {isCall ? "Call" : "Put"}: ${price}</p>}
        </CardContent>
      </Card>

      <Card className="bg-zinc-800 border-zinc-700">
        <CardContent className="p-6">
          <h2 className="text-xl font-bold mb-4">{isCall ? "Call" : "Put"} vs Precio del Activo</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData} key={isCall ? "call" : "put"}>
              <XAxis dataKey="S" stroke="#ccc" label={{ value: 'Precio del Activo (S)', position: 'insideBottom', offset: -5 }} />
              <YAxis stroke="#ccc" label={{ value: `Precio del ${isCall ? "Call" : "Put"}`, angle: -90, position: 'insideLeft' }} />
              <CartesianGrid strokeDasharray="3 3" stroke="#444" />
              <Tooltip contentStyle={{ backgroundColor: "#222", border: "none" }} />
              <ReferenceLine x={S} stroke="#22d3ee" strokeDasharray="4 4" label={{ position: 'top', value: `S = ${S}`, fill: '#22d3ee' }} />
              <Line type="monotone" dataKey="Value" stroke="#4f46e5" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
