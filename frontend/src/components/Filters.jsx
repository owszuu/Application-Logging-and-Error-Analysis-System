export default function Filters({ filters, setFilters }) {
    return (
      <div>
        <h3>Filters</h3>
  
        <label>Service:</label>
        <input
          value={filters.service}
          onChange={(e) => setFilters({ ...filters, service: e.target.value })}
        />
  
        <label>Level:</label>
        <select
          value={filters.level}
          onChange={(e) => setFilters({ ...filters, level: e.target.value })}
        >
          <option value="">All</option>
          <option value="INFO">INFO</option>
          <option value="WARNING">WARNING</option>
          <option value="ERROR">ERROR</option>
        </select>
      </div>
    );
  }
  