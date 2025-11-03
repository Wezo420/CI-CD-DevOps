import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-950 to-slate-900">
      <div className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto text-center space-y-6">
          <h1 className="text-5xl font-bold text-white mb-4">Medical Records Security Dashboard</h1>
          <p className="text-xl text-slate-300 mb-8">
            DevSecOps-integrated security monitoring for healthcare applications
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/dashboard">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                View Security Dashboard
              </Button>
            </Link>
            <Link href="/documentation">
              <Button size="lg" variant="outline">
                View Setup Guide
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
