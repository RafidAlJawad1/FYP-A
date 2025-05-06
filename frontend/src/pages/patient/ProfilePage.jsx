import { useState, useEffect } from 'react';
import axios from 'axios';

function ProfilePage() {
    const [profile, setProfile] = useState({ name: '', email: '', age: '', gender: '' });

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/profile')
            .then(res => setProfile(res.data));
    }, []);

    const handleUpdate = () => {
        axios.post('http://127.0.0.1:8000/api/profile/update', profile)
            .then(() => alert('Profile updated successfully'))
            .catch(() => alert('Update failed'));
    };

    return (
        <div>
            <h2>My Profile</h2>
            <label>Name: <input value={profile.name} disabled /></label><br />
            <label>Email: <input value={profile.email} disabled /></label><br />
            <label>Age: <input value={profile.age} onChange={e => setProfile({ ...profile, age: e.target.value })} /></label><br />
            <label>Gender:
                <select value={profile.gender} onChange={e => setProfile({ ...profile, gender: e.target.value })}>
                    <option value="">Select</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                </select>
            </label><br />
            <button onClick={handleUpdate}>Update Profile</button>
        </div>
    );
}

export default ProfilePage;
