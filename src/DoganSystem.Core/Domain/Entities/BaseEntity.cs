using System;
using Volo.Abp.Domain.Entities;

namespace DoganSystem.Core.Domain.Entities
{
    public abstract class BaseEntity<TKey> : Entity<TKey>
    {
        public DateTime CreationTime { get; set; }
        public DateTime? LastModificationTime { get; set; }
        public Guid? CreatorId { get; set; }
        public Guid? LastModifierId { get; set; }
        public bool IsDeleted { get; set; }
        public DateTime? DeletionTime { get; set; }
        public Guid? DeleterId { get; set; }
    }
}
