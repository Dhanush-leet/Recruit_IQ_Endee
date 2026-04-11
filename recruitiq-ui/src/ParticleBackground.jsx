import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { PerspectiveCamera, Float, Stars } from '@react-three/drei'
import * as THREE from 'three'

function ParticleField({ count = 1500 }) {
  const points = useMemo(() => {
    const p = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      p[i * 3] = (Math.random() - 0.5) * 100
      p[i * 3 + 1] = (Math.random() - 0.5) * 100
      p[i * 3 + 2] = (Math.random() - 0.5) * 100
    }
    return p
  }, [count])

  const ref = useRef()
  useFrame((state) => {
    ref.current.rotation.y = state.clock.getElapsedTime() * 0.05
    ref.current.rotation.x = state.clock.getElapsedTime() * 0.02
  })

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={points.length / 3}
          array={points}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.15}
        color="#7b61ff"
        transparent
        opacity={0.4}
        sizeAttenuation
      />
    </points>
  )
}

function CentralGlow() {
    return (
        <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
            <mesh>
                <sphereGeometry args={[2, 64, 64]} />
                <meshBasicMaterial color="#7b61ff" transparent opacity={0.1} />
            </mesh>
            <mesh scale={1.2}>
                <sphereGeometry args={[2, 64, 64]} />
                <meshBasicMaterial color="#ffffff" transparent opacity={0.05} />
            </mesh>
        </Float>
    )
}

export default function ParticleBackground() {
  return (
    <div className="fixed inset-0 z-0 bg-[#050505]">
      {/* Cinematic Vignette */}
      <div className="absolute inset-0 z-10 vignette pointer-events-none" />
      <div className="absolute inset-0 z-10 edge-glow pointer-events-none" />
      
      {/* Horizontal Light Streak (Gargantua style) */}
      <div className="absolute top-1/2 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-space-accent/40 to-transparent blur-[2px] z-10 opacity-30" />
      <div className="absolute top-1/2 left-0 w-full h-[10px] bg-gradient-to-r from-transparent via-space-accent/10 to-transparent blur-[10px] z-10 opacity-20" />

      <Canvas dpr={[1, 2]}>
        <PerspectiveCamera makeDefault position={[0, 0, 40]} fov={60} />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#7b61ff" />
        
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
        <ParticleField count={2000} />
        <CentralGlow />
        
        <fog attach="fog" args={['#050505', 30, 90]} />
      </Canvas>
    </div>
  )
}
