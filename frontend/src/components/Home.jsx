import { useState, useEffect } from 'react'
import axios from 'axios'
import { BookOpen, Briefcase, ChevronRight, User, MapPin, Phone, Github, Linkedin, Globe, Mail, ExternalLink } from 'lucide-react'
import { API_BASE_URL } from '../config'

const Home = ({ token }) => {
    const [profile, setProfile] = useState(null)
    const [recommendations, setRecommendations] = useState({ courses: [], jobs: [] })
    const [loading, setLoading] = useState(true)
    const [saving, setSaving] = useState(false)
    const [showForm, setShowForm] = useState(false)

    const [formData, setFormData] = useState({
        full_name: '',
        skills: '',
        experience: '',
        education: '',
        summary: '',
        phone: '',
        location: '',
        github_url: '',
        linkedin_url: '',
        portfolio_url: '',
        languages: ''
    })

    useEffect(() => {
        fetchProfile()
    }, [token])

    const fetchProfile = async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/users/me`, {
                headers: { Authorization: `Bearer ${token}` }
            })
            if (response.data.profile) {
                const p = response.data.profile
                setProfile(p)
                setFormData({
                    full_name: p.full_name || '',
                    skills: p.skills || '',
                    experience: p.experience || '',
                    education: p.education || '',
                    summary: p.summary || '',
                    phone: p.phone || '',
                    location: p.location || '',
                    github_url: p.github_url || '',
                    linkedin_url: p.linkedin_url || '',
                    portfolio_url: p.portfolio_url || '',
                    languages: p.languages || ''
                })
                fetchRecommendations()
            } else {
                setShowForm(true)
                setLoading(false)
            }
        } catch (err) {
            console.error(err)
            setLoading(false)
        }
    }

    const fetchRecommendations = async (force = false) => {
        setLoading(true)
        try {
            const response = await axios.get(`${API_BASE_URL}/recommendations${force ? '?refresh=true' : ''}`, {
                headers: { Authorization: `Bearer ${token}` }
            })
            setRecommendations(response.data)
        } catch (err) {
            console.error(err)
        } finally {
            setLoading(false)
        }
    }

    const handleFormSubmit = async (e) => {
        e.preventDefault()
        setSaving(true)
        // Clear existing recommendations immediately to show loading state after save
        setRecommendations({ courses: [], jobs: [] })
        try {
            await axios.post(`${API_BASE_URL}/profile`, formData, {
                headers: { Authorization: `Bearer ${token}` }
            })
            setShowForm(false)
            await fetchProfile()
        } catch (err) {
            console.error(err)
            alert("Failed to save profile")
        } finally {
            setSaving(false)
        }
    }

    const handleRefreshRecommendations = () => {
        setRecommendations({ courses: [], jobs: [] })
        fetchRecommendations(true)
    }

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    return (
        <div className="container">
            {/* Header Section */}
            <section style={{ marginBottom: '3rem' }}>
                <div className="glass-card" style={{ padding: '2.5rem' }}>
                    {!showForm ? (
                        <div style={{ display: 'flex', gap: '3rem', flexWrap: 'wrap', alignItems: 'center' }}>
                            <div style={{ flex: '0 0 auto', width: '120px', height: '120px', borderRadius: '30px', background: 'linear-gradient(135deg, var(--primary), var(--secondary))', display: 'flex', justifyContent: 'center', alignItems: 'center', boxShadow: '0 10px 25px rgba(99, 102, 241, 0.3)' }}>
                                <User size={56} color="white" />
                            </div>
                            <div style={{ flex: '1 1 300px' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                    <div>
                                        <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>{profile?.full_name || "New Professional"}</h1>
                                        <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                                            {profile?.location && <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}><MapPin size={16} /> {profile.location}</span>}
                                            {profile?.phone && <span style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}><Phone size={16} /> {profile.phone}</span>}
                                        </div>
                                    </div>
                                    <button onClick={() => setShowForm(true)} className="btn btn-primary">
                                        Edit Portfolio
                                    </button>
                                </div>
                                <p style={{ color: 'var(--text-muted)', marginTop: '1.5rem', lineHeight: '1.6', fontSize: '1.05rem', maxWidth: '800px' }}>
                                    {profile?.summary || "Share your journey to unlock AI-powered career paths."}
                                </p>

                                <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
                                    {profile?.linkedin_url && <a href={profile.linkedin_url} target="_blank" rel="noreferrer" className="badge" style={{ padding: '0.5rem 1rem', background: 'rgba(10, 102, 194, 0.1)', color: '#0a66c2' }}><Linkedin size={16} /> LinkedIn</a>}
                                    {profile?.github_url && <a href={profile.github_url} target="_blank" rel="noreferrer" className="badge" style={{ padding: '0.5rem 1rem', background: 'rgba(0,0,0,0.1)' }}><Github size={16} /> GitHub</a>}
                                    {profile?.portfolio_url && <a href={profile.portfolio_url} target="_blank" rel="noreferrer" className="badge" style={{ padding: '0.5rem 1rem', background: 'rgba(168, 85, 247, 0.1)', color: 'var(--secondary)' }}><Globe size={16} /> Website</a>}
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                                <h2>Professional Profile Setup</h2>
                                {profile && <button onClick={() => setShowForm(false)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>Close Editor</button>}
                            </div>
                            <form onSubmit={handleFormSubmit}>
                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginBottom: '1.5rem' }}>
                                    <div className="input-group">
                                        <label>Full Name</label>
                                        <input name="full_name" value={formData.full_name} onChange={handleInputChange} required placeholder="e.g. Sarath Chandiran" />
                                    </div>
                                    <div className="input-group">
                                        <label>Current Location</label>
                                        <input name="location" value={formData.location} onChange={handleInputChange} placeholder="e.g. Chennai, India" />
                                    </div>
                                    <div className="input-group">
                                        <label>Phone Number</label>
                                        <input name="phone" value={formData.phone} onChange={handleInputChange} placeholder="+91 9876543210" />
                                    </div>
                                    <div className="input-group">
                                        <label>Education Details</label>
                                        <input name="education" value={formData.education} onChange={handleInputChange} required placeholder="B.E. Robotics at Rajalakshmi Eng College" />
                                    </div>
                                </div>

                                <div className="input-group">
                                    <label>Technical Skills (comma separated)</label>
                                    <input name="skills" value={formData.skills} onChange={handleInputChange} required placeholder="React, Python, ROS2, PCB Design, SQL" />
                                </div>

                                <div className="input-group">
                                    <label>Languages Known</label>
                                    <input name="languages" value={formData.languages} onChange={handleInputChange} placeholder="English (Proficient), Tamil (Native)" />
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.5rem' }}>
                                    <div className="input-group">
                                        <label>LinkedIn URL</label>
                                        <input name="linkedin_url" value={formData.linkedin_url} onChange={handleInputChange} placeholder="https://linkedin.com/in/..." />
                                    </div>
                                    <div className="input-group">
                                        <label>GitHub URL</label>
                                        <input name="github_url" value={formData.github_url} onChange={handleInputChange} placeholder="https://github.com/..." />
                                    </div>
                                    <div className="input-group">
                                        <label>Portfolio URL</label>
                                        <input name="portfolio_url" value={formData.portfolio_url} onChange={handleInputChange} placeholder="https://yourwebsite.com" />
                                    </div>
                                </div>

                                <div className="input-group">
                                    <label>Professional Experience & Projects</label>
                                    <textarea name="experience" value={formData.experience} onChange={handleInputChange} required placeholder="Describe your key internships, personal projects, or work history..." rows="4" />
                                </div>

                                <div className="input-group">
                                    <label>Career Objective / Summary</label>
                                    <textarea name="summary" value={formData.summary} onChange={handleInputChange} placeholder="Briefly state your career goals and what you're looking for..." rows="3" />
                                </div>

                                <div style={{ display: 'flex', gap: '1rem' }}>
                                    <button type="submit" className="btn btn-primary" disabled={saving} style={{ padding: '0.8rem 2rem' }}>
                                        {saving ? "Optimizing Profile..." : "Publish & Generate Insights"}
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}
                </div>
            </section>

            {profile && !showForm && (
                <>
                    <div className="grid" style={{ marginBottom: '4rem' }}>
                        <div className="glass-card" style={{ padding: '1.5rem' }}>
                            <h3 style={{ fontSize: '1rem', color: 'var(--primary)', marginBottom: '1.2rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Core Expertise</h3>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                {profile.skills.split(',').map((skill, i) => (
                                    <span key={i} className="badge" style={{ background: 'var(--glass)', border: '1px solid rgba(255,255,255,0.1)' }}>{skill.trim()}</span>
                                ))}
                            </div>
                        </div>
                        <div className="glass-card" style={{ padding: '1.5rem' }}>
                            <h3 style={{ fontSize: '1rem', color: 'var(--secondary)', marginBottom: '1.2rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Known Languages</h3>
                            <p style={{ fontSize: '1.1rem' }}>{profile.languages || "Not specified"}</p>
                        </div>
                    </div>

                    {loading ? (
                        <div style={{ textAlign: 'center', padding: '5rem', background: 'var(--glass)', borderRadius: '20px' }}>
                            <div style={{ width: '40px', height: '40px', border: '3px solid var(--primary)', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite', margin: '0 auto 1.5rem' }}></div>
                            <p style={{ fontSize: '1.2rem', fontWeight: '500' }}>AI is curating your personalized career path...</p>
                        </div>
                    ) : (
                        <>
                            <section style={{ marginBottom: '4rem' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                                    <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.8rem', fontSize: '1.8rem' }}>
                                        <BookOpen size={32} color="var(--primary)" /> Upskilling Roadmap
                                    </h2>
                                    <button onClick={handleRefreshRecommendations} className="btn" style={{ background: 'var(--glass)', fontSize: '0.8rem', padding: '0.5rem 1rem' }}>
                                        Regenerate Suggestions
                                    </button>
                                </div>
                                <div className="grid">
                                    {recommendations.courses.map((course, i) => (
                                        <div key={i} className="glass-card" style={{ padding: '0', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                                            <div style={{ height: '140px', background: 'white', display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '1.5rem' }}>
                                                <img src={course.banner_url} alt={course.platform} style={{ maxWidth: '80%', maxHeight: '80%', objectFit: 'contain' }} />
                                            </div>
                                            <div style={{ padding: '1.5rem', flex: 1, display: 'flex', flexDirection: 'column' }}>
                                                <span style={{ fontSize: '0.8rem', color: 'var(--primary)', fontWeight: '700', textTransform: 'uppercase' }}>{course.platform}</span>
                                                <h3 style={{ margin: '0.8rem 0', minHeight: '3.5rem', fontSize: '1.2rem', lineHeight: '1.4' }}>{course.title}</h3>
                                                <div style={{ marginBottom: '2rem' }}>
                                                    {(() => {
                                                        const tags = course.tags || "";
                                                        const tagList = Array.isArray(tags) ? tags : tags.split(',');
                                                        return tagList.map((tag, j) => (
                                                            <span key={j} className="badge" style={{ fontSize: '0.7rem', opacity: 0.8 }}>{tag.trim()}</span>
                                                        ));
                                                    })()}
                                                </div>
                                                <a href={course.link} target="_blank" rel="noreferrer" className="btn btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: 'auto' }}>
                                                    Explore Course <ExternalLink size={18} />
                                                </a>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </section>

                            <section>
                                <h2 style={{ marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.8rem', fontSize: '1.8rem' }}>
                                    <Briefcase size={32} color="var(--secondary)" /> Strategic Placements
                                </h2>
                                <div className="grid">
                                    {recommendations.jobs.map((job, i) => (
                                        <div key={i} className="glass-card" style={{ borderLeft: '4px solid var(--secondary)' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                                <div>
                                                    <h3 style={{ fontSize: '1.4rem', marginBottom: '0.3rem' }}>{job.title}</h3>
                                                    <p style={{ color: 'var(--primary)', fontWeight: '600', fontSize: '1.1rem' }}>{job.company}</p>
                                                </div>
                                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                                                    <MapPin size={16} /> {job.location}
                                                </div>
                                            </div>
                                            <p style={{ margin: '1.5rem 0', fontSize: '0.95rem', color: 'var(--text-muted)', lineHeight: '1.6' }}>
                                                {job.description}
                                            </p>
                                            <div style={{ marginBottom: '2rem' }}>
                                                <p style={{ fontSize: '0.85rem', fontWeight: '700', marginBottom: '0.8rem', color: 'var(--text-muted)' }}>MANDATORY COMPETENCIES:</p>
                                                {(() => {
                                                    const skills = job.required_skills || "";
                                                    const skillList = Array.isArray(skills) ? skills : skills.split(',');
                                                    return skillList.map((skill, j) => (
                                                        <span key={j} className="badge" style={{ fontSize: '0.75rem', background: 'rgba(99, 102, 241, 0.05)' }}>{skill.trim()}</span>
                                                    ));
                                                })()}
                                            </div>
                                            <a href={job.link} target="_blank" rel="noreferrer" className="btn btn-primary" style={{ width: '100%', justifyContent: 'center', background: 'linear-gradient(135deg, var(--secondary), var(--primary))' }}>
                                                View Opportunity <ExternalLink size={18} />
                                            </a>
                                        </div>
                                    ))}
                                </div>
                            </section>
                        </>
                    )}
                </>
            )}

            <style>{`
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    )
}

export default Home
