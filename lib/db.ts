// Database utility for querying security data
// Supports Neon, Supabase, and any PostgreSQL-compatible database
import { neon } from "@neondatabase/serverless"

let sqlClient: any = null

export async function getDatabase() {
  if (!sqlClient && process.env.DATABASE_URL) {
    sqlClient = neon(process.env.DATABASE_URL)
  }
  return sqlClient
}

// Security metrics queries
export async function getSecurityMetrics() {
  const sql = await getDatabase()
  if (!sql) return null

  try {
    const result = await sql`
      SELECT 
        COALESCE(SUM(CASE WHEN severity = 'CRITICAL' THEN 1 ELSE 0 END), 0) as critical_issues,
        COALESCE(SUM(CASE WHEN severity = 'HIGH' THEN 1 ELSE 0 END), 0) as high_issues,
        COALESCE(SUM(CASE WHEN severity = 'MEDIUM' THEN 1 ELSE 0 END), 0) as medium_issues,
        COALESCE(SUM(CASE WHEN severity = 'LOW' THEN 1 ELSE 0 END), 0) as low_issues,
        COALESCE(COUNT(DISTINCT scan_id), 0) as scans_24h,
        COALESCE(AVG(scan_score), 0) as security_score,
        COALESCE(MAX(updated_at), NOW()) as latest_scan
      FROM vulnerabilities
      WHERE created_at > NOW() - INTERVAL '24 hours'
    `
    return result[0]
  } catch (error) {
    console.error("Database error:", error)
    return null
  }
}

export async function getVulnerabilities(limit = 10) {
  const sql = await getDatabase()
  if (!sql) return []

  try {
    const result = await sql`
      SELECT 
        id,
        title,
        description,
        severity,
        file_path,
        line_number,
        cvss_score,
        cwe_id,
        status
      FROM vulnerabilities
      WHERE status = 'OPEN'
      ORDER BY cvss_score DESC, created_at DESC
      LIMIT ${limit}
    `
    return result
  } catch (error) {
    console.error("Database error:", error)
    return []
  }
}

export async function getRecentScans(limit = 5) {
  const sql = await getDatabase()
  if (!sql) return []

  try {
    const result = await sql`
      SELECT 
        scan_id,
        scan_type,
        scan_status as status,
        start_time,
        end_time,
        total_issues as issues
      FROM security_scans
      ORDER BY created_at DESC
      LIMIT ${limit}
    `
    return result
  } catch (error) {
    console.error("Database error:", error)
    return []
  }
}

export async function getComplianceStatus() {
  const sql = await getDatabase()
  if (!sql) return []

  try {
    const result = await sql`
      SELECT 
        id,
        compliance_framework as framework,
        check_name,
        check_status as status,
        last_check
      FROM compliance_checks
      ORDER BY compliance_framework, check_name
    `
    return result
  } catch (error) {
    console.error("Database error:", error)
    return []
  }
}

export async function getSecurityTrends(days = 30) {
  const sql = await getDatabase()
  if (!sql) return []

  try {
    const result = await sql`
      SELECT 
        metric_date,
        average_scan_score as score,
        total_vulnerabilities as vulnerabilities
      FROM security_metrics
      WHERE metric_date >= NOW()::date - INTERVAL '${days} days'
      ORDER BY metric_date ASC
    `
    return result
  } catch (error) {
    console.error("Database error:", error)
    return []
  }
}
