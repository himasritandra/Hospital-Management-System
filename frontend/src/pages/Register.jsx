import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    phone: '',
    password: '',
    confirm: '',
  });
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (form.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }
    if (form.password !== form.confirm) {
      setError('Passwords do not match.');
      return;
    }

    setSubmitting(true);
    try {
      const { confirm, ...data } = form;
      await register(data);
      navigate('/dashboard');
    } catch (err) {
      const data = err.response?.data;
      if (data && typeof data === 'object') {
        setError(Object.values(data).flat().join(' '));
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1>Hospital Management System</h1>
        <h2>Patient Registration</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <label>First name</label>
          <input name="first_name" value={form.first_name} onChange={handleChange} />

          <label>Last name</label>
          <input name="last_name" value={form.last_name} onChange={handleChange} />

          <label>Username</label>
          <input name="username" value={form.username} onChange={handleChange} required />

          <label>Email</label>
          <input type="email" name="email" value={form.email} onChange={handleChange} required />

          <label>Phone</label>
          <input name="phone" value={form.phone} onChange={handleChange} />

          <label>Password</label>
          <input type="password" name="password" value={form.password} onChange={handleChange} required />

          <label>Confirm password</label>
          <input type="password" name="confirm" value={form.confirm} onChange={handleChange} required />

          <button type="submit" disabled={submitting}>
            {submitting ? 'Creating account...' : 'Register'}
          </button>
        </form>
        <p className="link">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
}