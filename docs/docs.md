# Cattendance Documentation

Complete official documentation for the Cattendance Class Attendance System with QR Code Scanning.

---

## Documentation Index

### 📖 Core Documentation

1. **[System Overview](system-overview.md)**
   - Project purpose and features
   - System architecture
   - Technology stack
   - Team information

2. **[Installation Guide](installation.md)**
   - Prerequisites and requirements
   - Development environment setup
   - Production deployment (Render + Supabase)
   - Configuration and environment variables

3. **[User Guide](user-guide.md)**
   - Complete walkthrough for all user roles:
     - Student features and workflows
     - Teacher features and workflows
     - Admin features and workflows
   - Step-by-step instructions with screenshots

4. **[Admin Manual](admin-manual.md)**
   - User management
   - System maintenance
   - Troubleshooting procedures
   - Security best practices
   - Backup and recovery

5. **[Developer Documentation](developer-docs.md)**
   - Project structure and architecture
   - Database models and relationships
   - Views and business logic
   - Templates and static files
   - Git workflow and conventions
   - Testing and debugging

6. **[API Reference](api-reference.md)**
   - Complete endpoint documentation
   - Request/response formats
   - Authentication requirements
   - Error codes and handling

7. **[Troubleshooting Guide](troubleshooting.md)**
   - Common issues and solutions
   - Database errors
   - Deployment problems
   - Authentication issues
   - QR code problems
   - CSV operations
   - Performance optimization

---

## Quick Links

### For Students
- [How to Register](user-guide.md#student-registration)
- [How to View Classes](user-guide.md#viewing-enrolled-classes)
- [How to Scan QR Codes](user-guide.md#marking-attendance-via-qr-code)
- [How to Check Attendance](user-guide.md#viewing-attendance-history)

### For Teachers
- [How to Create Classes](user-guide.md#creating-a-new-class)
- [How to Add Students](user-guide.md#adding-students-to-a-class)
- [How to Start a Session](user-guide.md#creating-an-attendance-session)
- [How to Generate QR Codes](user-guide.md#generating-qr-code-for-attendance)
- [How to Export Attendance](user-guide.md#exporting-attendance-records)

### For Administrators
- [How to Create Teacher Accounts](admin-manual.md#creating-teacher-accounts)
- [How to View All Users](admin-manual.md#viewing-students-and-teachers)
- [How to Troubleshoot Issues](admin-manual.md#troubleshooting-common-issues)

### For Developers
- [Project Setup](installation.md#development-setup)
- [Database Schema](developer-docs.md#database-schema)
- [Code Structure](developer-docs.md#project-structure)
- [API Endpoints](api-reference.md)
- [Common Errors](troubleshooting.md)

---

## Getting Started

### New to Cattendance?

1. **Read the [System Overview](system-overview.md)** to understand what the system does
2. **Follow the [Installation Guide](installation.md)** to set up your environment
3. **Check the [User Guide](user-guide.md)** for your specific role
4. **Bookmark the [Troubleshooting Guide](troubleshooting.md)** for when issues arise

### Developers

1. **Read [Developer Documentation](developer-docs.md)** for architecture details
2. **Review [API Reference](api-reference.md)** for endpoint specifications
3. **Follow [Installation Guide](installation.md)** to set up development environment
4. **Use [Troubleshooting Guide](troubleshooting.md)** for debugging

### Administrators

1. **Read [Admin Manual](admin-manual.md)** for system administration tasks
2. **Check [User Guide](user-guide.md#admin-workflows)** for admin features
3. **Review [Troubleshooting Guide](troubleshooting.md)** for issue resolution

---

## Documentation Format

All documentation is written in **Markdown** format for easy reading on:
- GitHub repositories
- Documentation websites (MkDocs, Docusaurus, etc.)
- Text editors (VS Code, Atom, etc.)
- Web browsers (with Markdown viewers)

---

## System Requirements

### For Users
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Stable internet connection
- Smartphone with camera (for QR code scanning)
- WiFi network access (same network as teacher for attendance)

### For Development
- Python 3.8 or higher
- Node.js 16+ and npm (for Tailwind CSS)
- PostgreSQL 12+ or Supabase account
- Git for version control
- Code editor (VS Code recommended)

### For Production Deployment
- Render.com account (or similar PaaS)
- Supabase account (or PostgreSQL database)
- Custom domain (optional)

---

## Key Features

✅ **Role-Based Authentication** - Student, Teacher, Admin dashboards  
✅ **QR Code Attendance** - Generate time-limited QR codes, scan to mark present  
✅ **Network Verification** - Ensures students are physically in class  
✅ **Class Management** - Create classes, manage schedules, track enrollments  
✅ **Session Tracking** - Create attendance sessions with QR code generation  
✅ **CSV Import/Export** - Bulk student enrollment and attendance exports  
✅ **Attendance Analytics** - View statistics and attendance rates  
✅ **Manual Override** - Teachers can manually mark attendance  
✅ **Mobile Responsive** - Works on desktop, tablet, and mobile devices  
✅ **Secure** - Password strength enforcement, CSRF protection, session management

---

## Technology Stack

**Backend:**
- Django 5.2.6 (Python web framework)
- PostgreSQL via Supabase (Database)
- WhiteNoise (Static file serving)

**Frontend:**
- Tailwind CSS v4 (Styling)
- Vanilla JavaScript (Interactivity)
- Django Templates (Server-side rendering)

**Infrastructure:**
- Render.com (Hosting)
- Supabase (Database hosting)
- Git/GitHub (Version control)

**Additional Libraries:**
- segno (QR code generation)
- psycopg2-binary (PostgreSQL adapter)
- gunicorn (WSGI HTTP server)
- python-dotenv (Environment variables)

---

## Support and Contact

### Reporting Issues

1. **Check [Troubleshooting Guide](troubleshooting.md)** first
2. **Search existing issues** on GitHub
3. **Create new issue** with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots (if applicable)
   - Error messages

### Development Team

- **Project Lead:** [Axel Gerome](https://github.com/Liiii-01)
- **Contributors:** See [CONTRIBUTING.md](../CONTRIBUTING.md)
- **GitHub Repository:** [github.com/Liiii-01/cattendance-v2](https://github.com/Liiii-01/cattendance-v2)

### Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Git workflow
- Branching conventions
- Code standards
- Pull request process

---

## License

[Specify your license here]

---

## Version History

- **v2.0** - Current version
  - QR code attendance system
  - Network verification
  - Role-based dashboards
  - CSV import/export
  - Tailwind CSS v4

- **v1.0** - Initial release
  - Basic attendance tracking
  - Manual marking only

---

## External Resources

### Django Documentation
- Official Django Docs: https://docs.djangoproject.com/
- Django Tutorial: https://docs.djangoproject.com/en/stable/intro/tutorial01/

### Deployment Guides
- Render.com Docs: https://render.com/docs
- Supabase Docs: https://supabase.com/docs

### Frontend Resources
- Tailwind CSS: https://tailwindcss.com/docs
- JavaScript MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript

### Development Tools
- Git Documentation: https://git-scm.com/doc
- VS Code: https://code.visualstudio.com/docs

---

## Changelog

### Latest Updates

**December 2024:**
- ✅ Complete documentation overhaul
- ✅ Added comprehensive troubleshooting guide
- ✅ Enhanced API reference with all endpoints
- ✅ Improved developer documentation
- ✅ Added detailed user guides for all roles

**Previous Updates:**
- See Git commit history for detailed changes

---

## Documentation Maintenance

This documentation is maintained by the development team and updated regularly.

**Last Updated:** December 2024  
**Documentation Version:** 2.0  
**Application Version:** 2.0

---

## Feedback

We welcome feedback on this documentation!

- **Unclear instructions?** Open an issue
- **Missing information?** Submit a pull request
- **Found errors?** Report them on GitHub

---

**Thank you for using Cattendance!** 🎓📱

For any questions or support, please refer to the relevant documentation section or contact the development team.
