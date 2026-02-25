import { Link } from 'react-router-dom'
import { Briefcase, LogOut, User as UserIcon } from 'lucide-react'

const Navbar = ({ token, logout }) => {
    return (
        <nav className="navbar">
            <Link to="/" className="logo" style={{ textDecoration: 'none' }}>
                <Briefcase className="logo-icon" />
                SkillMatrix
            </Link>
            <div className="nav-links" style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                {token ? (
                    <>
                        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Dashboard</Link>
                        <button onClick={logout} className="btn btn-primary" style={{ padding: '0.5rem 1rem' }}>
                            <LogOut size={18} /> Logout
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" style={{ color: 'white', textDecoration: 'none' }}>Login</Link>
                        <Link to="/signup" className="btn btn-primary" style={{ textDecoration: 'none', padding: '0.5rem 1rem' }}>Signup</Link>
                    </>
                )}
            </div>
        </nav>
    )
}

export default Navbar
